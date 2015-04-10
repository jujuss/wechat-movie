import pycurl
url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=nfpeeRAwrS_lmNeRnhH4vFtbejmGof1Hy_Keik3Ox2w82mpmzkFIjP6YBNFtL-E6G1VYzEGTGUK141qjIa_agW15JVphGHlHs_Yips8ybRc&type=image"

file1 = "p2225660666.jpg"
file2 = 'p2235593851.jpg'
field = "uploadFile"
c = pycurl.Curl()
c.setopt(c.POST, 1)
c.setopt(c.URL, url)
c.setopt(c.HTTPPOST, [('', (c.FORM_FILE, file1))])
# c.setopt(c.VERBOSE, 1)
c.perform()
c.setopt(c.HTTPPOST, [('', (c.FORM_FILE, file2))])
c.perform()
c.close()
