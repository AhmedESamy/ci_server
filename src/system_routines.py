import os


#repo="https://github.com/AhmedESamy/Launch_Interceptor"
def clone_and_run(data):
    reponame = data["repository"]["name"]
    os.system("cd src/testingdir")
    os.system("git clone "+str(os.environ.get("TEST_TARGET_REPO")))
    os.system("cd "+reponame)
    os.system("pwd")
    os.system("pytest src/tests/")
    os.system("cd ..")
    os.system("sudo rm -r "+reponame)
    os.system("cd ..")
    return
    
    