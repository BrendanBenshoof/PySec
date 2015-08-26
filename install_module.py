
import os,sys

cachePath = "/home/brendan/secpy/lib/secPy"

def AddPath():
    sys.path.append(cachePath)


def ensure(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def install_package(path):
    import pymultihash as pmh
    os.chdir(path)
    paths = []
    for root, dir, files in os.walk("."):
            for item in files:
                if(len(item)>3 and item[-3:]==".py"):
                    path = root+"/"+item
                    hval = None
                    with open(path,"r") as fp:
                        data = fp.read()
                        hval = pmh.genHash(data,0x12)
                    paths.append((hval,path))
    cert = "\n".join(map(lambda x: " ".join(x),paths))
    certhash = pmh.genHash(cert,0x12)
    hashed_cert = certhash+"\n"+cert


    working_path = os.path.join(cachePath,certhash)
    #print("Working Path",working_path)
    ensure(working_path)
    with open(os.path.join(working_path,"certfile.txt"),"w") as fp:
        fp.write(hashed_cert)
    for h, fname in paths:
        dest = os.path.join(working_path,fname)
        dirname = os.path.dirname(dest)
        ensure(dirname)
        with open(fname,"r") as read_fp:
            with open(dest,"w") as write_fp:
                write_fp.write(read_fp.read())
    print("Package Name is:")
    print(certhash)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Adds files to a content address package library')
    parser.add_argument('path', type=str,
                       help='path to the root of a package')
    parser.add_argument('--cachePath',type=str, default="/usr/lib/secPy/",
                       help='changes the cache to which the package is stored')
    args = parser.parse_args()
    package_path = args.path
    cachePath = args.cachePath
    install_package(package_path)
