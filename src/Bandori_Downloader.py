import os
import re
import codecs
import requests
import urllib.error
import urllib.request

version = 2.0
AWSURL = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'
BGMURL = 'https://res.bandori.ga/assets/sound/'
GITHUBURL = 'https://raw.githubusercontent.com/MayaYamato/Bandori_Downloader/master/version'
VERSIONURL = 'https://raw.githubusercontent.com/esterTion/bangdream_master_db_diff/master/!dataVersion.txt'

os.chdir(os.path.dirname(os.path.abspath(__file__)))
download_dir_asset = os.getcwd()+r'\asset'
download_dir_bgm = os.getcwd()+r'\bgm'

print('Bandori_Downloader v'+str(version)+'\n')
print('Created By:VERSUS.log\n### Please comment or reply if you have any errors or qustions\n')
print('Twitter:@72G_VS\nBlog URL:https://raspberrypi422.mydns.jp\nGithub Repository:https://github.com/MayaYamato/Bandori_Downloader')
print('### Thanks to external links used in this tool ...\n')

def download_asset(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path,'wb') as f0:
            f0.write(data)
    except urllib.error.URLError as e:
        pass

def download_bgm(url,dst_path):
    try:
        download = requests.get(url)
        with open(dst_path,'wb') as f0:
            f0.write(download.content)
    except urllib.error.URLError as e:
        pass

def Version_Check_Update(url):
    print('Version Checking ... ')
    with urllib.request.urlopen(url) as response:
        html = response.read().decode() #responseで得たbyte列を変換
        exever = html[:-1]
    if float(exever) - float(version) > 0:
        print('New Version Released:'+str(exever)+'\n')
        tmp =input('Do you want to upgrade? yes or no\n>>')
        if tmp == 'yes':
            download_bgm(r'https://github.com/MayaYamato/Bandori_Downloader/releases/download/v'+str(exever)+r'/Bandori_Downloader.exe',dst_path)
            print('Download Complete')
            exit()
        elif tmp == 'no':
            pass
        else:
            pass
    else:
        print('Latest Version\n')

def ABI_Download(ver,tmp,OS,dst_path):
    print('\nABI Downloading:')
    if len(tmp) > 2:
        url = AWSURL +str(ver)+str(tmp)+'/'+str(OS)+r'/AssetBundleInfo'
    else:
        url = AWSURL +str(ver)+'/'+str(OS)+r'/AssetBundleInfo'
    download_asset(url, dst_path)
    print('ABI Download complete\nShaping ABI started')

### main source ###

### Version Check ##
Version_Check_Update(GITHUBURL)

### Asset or BGM ###
tmp = input('Which do you want Asset or BGM? \n (Asset ⇒ 0 Bgm ⇒ 1 )\n>>').rstrip()

### ABI/Asset Download ###
if int(tmp) == 0:

    if not os.path.exists(download_dir_asset):
        os.makedirs(download_dir_asset)

    ### ABI Version ###
    tmp =input('\nWhat version of ABI do you want?\n ex:latest version ⇒ 0\n ex:2.0.0.300(18 Aprir) ⇒ 1\n ex:3.0.0.500(19 Aprir) ⇒ 2\n ex:Direct Input\n>>').rstrip()
    if int(tmp) == 0:
        with urllib.request.urlopen(VERSIONURL) as response:
            html = response.read().decode() #responseで得たbyte列を変換
            ver = html[:-1]
        print(ver)
    elif int(tmp) == 1:
        ver = '2.0.0.300'
    elif int(tmp) == 2:
        ver = '3.0.0.500'
    else :
        ver = tmp

    ### OS Version ###
    tmp = input("\nWhich do you want Android or iOS? \n(Android ⇒ 0 iOS ⇒ 1 )\n>> ").rstrip()
    if int(tmp)==0:
        OS='Android'
    elif int(tmp)==1:
        OS='iOS'
    else :
        print('ERROR')

    ### ABI Shaping ###
    tmp = input("\nChoose Shaping ABI method\n###Choose Latest if you want to format the latest ABI,\n###Old is effective against ABI before 2020\n(Latest ⇒ 0 Old ⇒ 1)\n>> ").rstrip()
    
    if int(tmp)==0:
        tmp = input("Please enter the URL change character string. \n(This character string can be confirmed by packet capture etc. If you do not understand the meaning, ask the author)\nforexample:_p3HzsCWjkY\n>>").rstrip()
        filename = os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt')
        dst_path = os.path.join(download_dir_asset, filename)
        ABI_Download(ver,tmp,OS,dst_path)
    
        ### latest ABI Shaping ###
        if os.path.exists(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt'):
            os.remove(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt')
        with codecs.open(r'asset/AssetBundleInfo(raw) ver '+str(ver)+' .txt',"r","cp932","ignore") as lines:
            for line in lines:
                seiki = r'^(?!.*'+str(ver)+r').*$'
                txt0=re.sub(seiki,'',line)
                txt0=re.sub(r'^\n|\r','',txt0)
                txt0=re.sub(r'@.*?\n','\n',txt0)
                txt0=re.sub(r'@.*?\Z','\n',txt0)
                new_txt=re.sub(r'^[^a-z]?(.+)\x12.*?\n','https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+str(tmp)+'/'+str(OS)+r'/\1\n',txt0)
                with open(r'asset\AssetBundleInfo ver '+str(ver)+' .txt',"a") as f:
                    f.write(new_txt)

    elif int(tmp)==1:
        filename = os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt')
        dst_path = os.path.join(download_dir_asset, filename)
        ABI_Download(ver,tmp,OS,dst_path)

        ### OLD ABI Shaping ###
        if os.path.exists(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt'):
            os.remove(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt')
        with codecs.open(r'asset/AssetBundleInfo(raw) ver '+str(ver)+' .txt',"r","cp932","ignore") as lines:
            for line in lines:
                seiki = r'^(?!.*'+str(ver)+r').*$'
                txt0=re.sub(seiki,'',line)
                txt0=re.sub(r'^\n|\r','',txt0)
                txt0=re.sub(r'@.*?\n','\n',txt0)
                txt0=re.sub(r'@.*?\Z','\n',txt0)
                new_txt=re.sub(r'^[^a-z]?(.+)\x12.*?\n','https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/\1\n',txt0)
                with open(r'asset\AssetBundleInfo ver '+str(ver)+' .txt',"a") as f:
                    f.write(new_txt)
    else :
        print("ERROR")

    print("Complete\n")

    ### All Asset Download ###
    tmp = input("Do you want to download all asset?\n### But not recommended to download:Too many assets. yes ⇒ 0 no ⇒ 1\n>>")
    if int(tmp) == 0 :
        print('Loading ABI')
        with open(r'asset/AssetBundleInfo ver '+str(ver)+' .txt') as lines:
            for line in lines:
                url = line.rstrip('\r\n')
                filename = os.path.basename(url)
                dst_path = os.path.join(download_dir_asset, filename)
                if os.path.exists(dst_path):
                    for n in range (1, 1000):
                        new_filename = str(filename)  + '(' + str(n) + ')'
                        dst_path = os.path.join(download_dir_asset, new_filename)
                        if not os.path.exists(dst_path):
                            download_asset(url, dst_path)
                            break
                        else:
                            continue
                else:
                    download_asset(url, dst_path)
        print("Download complete")
    elif int(tmp) == 1 :
        exit()
    else:
        exit()

### BGM Download ###
elif int(tmp) == 1:

    if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)

    print('Downloading BGM')
    filename = os.path.basename('bgm.json')
    dst_path = os.path.join(download_dir_bgm, filename)
    print(dst_path)
    print(filename)
    download_bgm(BGMURL, dst_path)

    with open(dst_path) as lines:
        for line in lines:
            m = re.search(r'bgm(.+)_rip', line)
            if m == None:
                continue
            else:
                url = BGMURL+str(m.group()[:-4])+'_rip/'+str(m.group()[:-4])+'.mp3'
                filename = os.path.basename(url)
                dst_path = os.path.join(download_dir_bgm, filename)
                print(url)
                if os.path.exists(dst_path):
                    continue
                else :
                    download_bgm(url, dst_path)
    os.remove(os.getcwd()+r'\bgm\bgm.json')

else:
    print('ERROR')