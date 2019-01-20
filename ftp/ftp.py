import sys
import ftplib
import os
from ftplib import FTP

___author___ = "patryk.damec@gmail.com"


def download_files_from_ftp(path, remote):
    """
    :param path: path to the files content on FTP.
    :param remote: path where to save the files.
    """
    try:
        ftp.cwd(path)
        os.chdir(remote)
        os.mkdir(remote[0:len(remote)-1]+path)
    except OSError:
        pass
    except ftplib.error_perm:
        print "error: could not change to "+path
        sys.exit("ending session")

    filelist=ftp.nlst()

    for file in filelist:
        try:
            ftp.cwd(path+file+"/")
            download_files_from_ftp(path+file+"/", remote)

        except ftplib.error_perm as e:
            print "Cannot access the folder's content" \
                  "Reason:{}".format(e)
            try:
                os.chdir(remote[0:len(remote) - 1] + path)
            except OSError:
                os.makedirs(remote[0:len(remote) - 1] + path)

            # Download all files that end with .txt
            if file.endswith('.txt'):
                ftp.retrbinary("RETR " + file, open(os.path.join(remote, file), "wb").write)
                print "{} is downloaded".format(file)
    return


if __name__ == "__main__":

    ftp = FTP('')
    ftp.login('')

    remote_path = ''
    local_path = ''

    download_files_from_ftp(remote_path, local_path)
