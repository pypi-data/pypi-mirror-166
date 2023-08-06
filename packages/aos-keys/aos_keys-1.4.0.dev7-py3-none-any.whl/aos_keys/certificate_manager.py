#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#
"""Install root and client certificates on different OSes."""
import os
import subprocess
import tempfile
from pathlib import Path

from aos_keys.common import ca_certificate, AosKeysError


def _execute_command(command):

    try:
        completed_process = subprocess.run(command, capture_output=False, env=os.environ.copy())
    except KeyboardInterrupt:
        raise AosKeysError('Operation interrupted by user')
    if completed_process.returncode == 0:
        return

    error = completed_process.stderr
    if not error and completed_process.stdout:
        error = completed_process.stdout
        if error:
            error = error.decode("utf8")
    print(completed_process.stderr)
    raise AosKeysError(f'Failed to install certificate:\n {error}')


def install_root_certificate_macos():
    """Install root certificate on current user's Trusted Root CA."""
    with ca_certificate() as server_certificate_path:
        print('We are going to add Aos Root certificate as trusted certificate.')
        print('The OS will ask your password to proceed with operation.')
        command = [
            'security',
            'add-trusted-cert',
            '-r',
            'trustRoot',
            str(server_certificate_path),
        ]
        _execute_command(command)


def install_root_certificate_windows():
    """Install root certificate on current user's Trusted Root CA."""
    with ca_certificate() as server_certificate_path:
        command = ['certutil', '-addstore', '-f', '-user', 'Root', server_certificate_path]
        _execute_command(command)


def install_root_certificate_linux():
    """Install root certificate on linux host."""
    command = ['dpkg', '-s', 'ca-certificates']
    completed_process = subprocess.run(command, capture_output=True)
    if completed_process.returncode > 0:
        raise AosKeysError(
            'Failed to install certificate. Required package missing',
            'Install update-ca-certificates first with command: sudo apt install ca-certificates',
        )

    command = ['dpkg', '-s', 'libnss3-tools']
    completed_process = subprocess.run(command, capture_output=True)
    if completed_process.returncode > 0:
        raise AosKeysError(
            'Failed to install certificate. Required package missing',
            'Install update-ca-certificates first with command: sudo apt install libnss3-tools',
        )

    with ca_certificate() as server_certificate_path:
        if not Path('/usr/local/share/ca-certificates').exists():
            command = ['sudo', 'mkdir', '/usr/local/share/ca-certificates']
            _execute_command(command)
        if not Path('/usr/local/share/ca-certificates/AosRootCA.crt').exists():
            command = ['sudo', 'cp', server_certificate_path, '/usr/local/share/ca-certificates/AosRootCA.crt']
            _execute_command(command)
        command = ['sudo', 'update-ca-certificates']
        _execute_command(command)

        with tempfile.NamedTemporaryFile() as password_file:
            # empty password file prevents asking password from stdin
            command = [
                'certutil',
                '-d', f'sql:{str(Path.home())}/.pki/nssdb',
                '-A', '-t', 'C',
                '-n', 'Aos root certificate',
                '-i', server_certificate_path,
                '-f', password_file.name,
            ]
            _execute_command(command)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12, BestAvailableEncryption, PrivateFormat

def add_password_to_pkcs12(filename_in: str, filename_out: str, password: bytes, friendly_name: bytes or None):
    with open(filename_in, 'rb') as file_handle:
        pkcs12_bytes = file_handle.read()
    key_certificates = pkcs12.load_pkcs12(pkcs12_bytes, None)

    # This code should be used after PR release https://github.com/pyca/cryptography/pull/7560/
    # encryption = (
    #     PrivateFormat.PKCS12.encryption_builder().
    #     kdf_rounds(50000).
    #     key_cert_algorithm(pkcs12.PBES.PBESv1SHA1And3KeyTripleDESCBC).
    #     hmac_hash(hashes.SHA1()).build(password)
    # )

    protected_pkcs12_bytes = pkcs12.serialize_key_and_certificates(
        friendly_name,
        key_certificates.key,
        key_certificates.cert.certificate,
        [cert.certificate for cert in key_certificates.additional_certs],
        BestAvailableEncryption(password),
        # encryption, # See comment above
    )
    with open(filename_out, 'wb') as file_handle:
        file_handle.write(protected_pkcs12_bytes)


def install_user_certificate_windows(certificate_path: Path):
    """Install client certificate to the Windows Personal store.

    Args:
        certificate_path: path to certificate which will be installed.
    """
    command = ['certutil', '-addstore', '-f', '-user', 'My', certificate_path]
    _execute_command(command)


def install_user_certificate_linux(certificate_path: Path):
    """Install client certificate to the Windows Personal store.

    Args:
        certificate_path: path to certificate which will be installed.
    """
    print('We are going to import your private key and certificate to browsers databases.')
    command = ['pk12util', '-d', f'sql:{str(Path.home())}/.pki/nssdb', '-i', certificate_path]
    _execute_command(command)


def install_user_certificate_macos(certificate_path: Path):
    """Install client certificate to the Windows Personal store.

    Args:
        certificate_path: path to certificate which will be installed.
    """
    password_protected_filename = str(certificate_path) + '.pswd'
    add_password_to_pkcs12(str(certificate_path), password_protected_filename, b'1234', None)

    command = [
        'security',
        'import',
        password_protected_filename,
        '-f',
        'pkcs12',
        '-P',
        '1234',
    ]
    _execute_command(command)
