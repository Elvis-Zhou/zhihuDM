# -*- coding:utf-8 -*-
#encoding = utf-8
import urllib, urllib2, cookielib, re, sys
import chardet,string,time,random,os
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

#url="http://status.renren.com/status/hot/list?word=%E4%BF%9D%E9%92%93%E4%BA%BA%E5%A3%AB%E7%99%BB%E5%B2%9B%E6%88%90%E5%8A%9F"
#htmlfile=urllib2.urlopen(url).read()
#print htmlfile
count=0
urllib2.socket.setdefaulttimeout(30)
#input=open("hotstatus.txt","r")
outputfilename1="finance%s.txt" % time.strftime("%y-%m-%d ",time.localtime(time.time()))
outputfilename2="rawfinance%s.txt" % time.strftime("%y-%m-%d",time.localtime(time.time()))
#out=open("hotstatus.txt","a")

out=open(outputfilename1,"a")
out2=open(outputfilename2,"a")
out3=open("question.txt","a")

class zhihu():
    def __init__(self):
        self.soup=""
        self.names=""
        self.dic={}
        self.quesitons=[]
        self.quesitonurls=[]
        self.answers=[]
        self.question=""
        self.cururl=""
        self.url="http://www.zhihu.com/"

        self.htmlfile=""
        self.requset=""

        self.q="金融"

        self.content=set()
        #把content从list改成set以去重
        #self.keyword="保钓人士登岛成功"
        self.charset="utf-8"
        self.cookie='_xsrf=a3ba8390ce764adaaf72ec7c408e6456; q_c0="ODg0OGFkYmMzNjI4ZWVlZGE5ZmRkMDU1NDRlOGI4Y2V8dFVpMlpGTnNiWERoeFBCbA==|1345908275|d54477a66a915d1e5cc41f1afb3127b95912f95c"; __utma=155987696.272003110.1345826185.1345826185.1345908280.2; __utmb=155987696.7.8.1345908321042; __utmc=155987696; __utmz=155987696.1345826185.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155987696.Logged%20In'
        try:
            cookie=cookielib.CookieJar()
            cookieProc=urllib2.HTTPCookieProcessor(cookie)
        except:
            raise
            #else:
        self.opener=urllib2.build_opener(cookieProc)
        urllib2.install_opener(self.opener)
    def generatepurl(self,q="金融",page=0):
        self.q=q
        url='http://www.zhihu.com/search/question?'
        #url='http://www.zhihu.com/search/question?q=%E9%87%91%E8%9E%8D&type1=question&page=2'
        postdata={
            'q':self.q,
            'type1':"question",
            'page':page
        }
        cookie=cookielib.CookieJar()
        cookieProc=urllib2.HTTPCookieProcessor(cookie)
        self.opener=urllib2.build_opener(cookieProc)
        urllib2.install_opener(self.opener)
        self.url=url+urllib.urlencode(postdata)
        self.requset=urllib2.Request(self.url)
        #self.requset.add_header("cookie",self.cookie)
        #self.file=urllib2.urlopen(req).read()
        print self.url
        return self.url

    def showurls(self,htmlfile):
        #testurl="http://www.zhihu.com/search/question?q=%E9%87%91%E8%9E%8D&type1=question&page=37"
        #self.htmlfile=self.getpage(testurl)
        if htmlfile:
            self.htmlfile=htmlfile

        self.soup=BeautifulSoup(self.htmlfile)
        url="http://www.zhihu.com"
        #questions=self.soup.find
        quesitons=self.soup.find_all("a",{"style":"display: inline-block;margin-bottom: 3px;font-size: 14px;","target":"_blank"})
        for q in quesitons:
            self.quesitons.append(q.text)
            self.question=q.text
            self.quesitonurls.append(url+q["href"])
            #self.cururl=url+q["href"]
        #print self.quesitons
        return self.quesitonurls

    def getpage(self,url):
        #self.keyword=keyword
        if url:
            self.url=url
        self.requset=urllib2.Request(self.url)
        self.requset.add_header("Cookie",self.cookie)
        self.requset.add_header("Host","www.zhihu.com")
        self.requset.add_header("Referer",self.cururl)
        self.requset.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1")
        i=0
        t=0
        while t==0:
            try:
                self.htmlfile=urllib2.urlopen(self.requset).read()
                if  self.htmlfile:
                    t=1
                    break
                else:
                    i+=1
                    #continue
            except :
                i+=1
            if i>=5:break

        #print self.htmlfile
        return self.htmlfile

    def dealcontent(self,questionlist=[],answercount=3):
        if questionlist:
            self.quesitonurls=questionlist

        for url in self.quesitonurls:
            self.cururl=url
            self.htmlfile=self.getpage(url)
            soup=BeautifulSoup(self.htmlfile,"lxml")

            while soup.find(text="请输入图中的数字："):
                print "\a"*10,
                #os.system("cmd ./beep.bat")
                print url+" 知乎要求输入验证码，请打开知乎输入"
                time.sleep(20)
                #这个是获取问题及答案的时候
                self.htmlfile=self.getpage(url)
                soup=BeautifulSoup(self.htmlfile,"lxml")

            #print soup
            self.question=soup.title.text[:-4]
            #print self.question
            answers=soup.find_all("div",{"class":"xajw xod"})
            keywords=soup.find_all("a",{"class":"xyk"})
            self.keyword=""
            for k in keywords:
                self.keyword+=k.text.strip()+" "
            print "关键词是: "+self.keyword
            #print answers
            if answers:
                self.answer=answers[0].text
            else:
                self.answer=u"这个问题没有一个好的答案"
            if answers:
                i=0
                for ans in answers:
                    self.answers.append(ans.text)
                    i+=1
                    if i>=answercount:break

            #print self.answer
            self.writetoaiml()
            self.writetorawfile()
            self.answers=[]
            time.sleep(random.randint(1,3))
        self.questionurls=[]
        self.answers=[]
        """
        html=open("test.html")
        htmlfile=""
        for i in html:
            htmlfile+=i
        soup=BeautifulSoup(htmlfile,"lxml")
        question=soup.title.text[:-4]

        answers=soup.find("div",{"class":"xajw xod"})
        print question
        print answers.text
        """
        return 1

    def dealquestions(self,startpage=31,maxpage=38,keyword="金融",answercount=3):
        for page in range(startpage,maxpage+1):
            print "now at page:"+str(page)
            self.quesitonurls=[]
            self.quesitons=[]
            url=self.generatepurl(keyword,page)
            htmlfile=self.getpage(url)
            soup=BeautifulSoup(htmlfile,"lxml")
            while soup.find_all(text="请输入图中的数字："):
                print "\a"*10,
                print url+" 知乎要求输入验证码，请打开知乎输入"
                #os.system("cmd ./beep.bat")
                time.sleep(20)
                #这个是获取问题列表URL的时候
                htmlfile=self.getpage(url)
                soup=BeautifulSoup(htmlfile,"lxml")

            self.showurls(htmlfile)
            self.dealcontent(answercount=answercount)

            for q in self.quesitons:
                out3.write(q+"\n")
            out3.flush()
            self.quesitons=[]
            print "sleep half a minute~~~"
            time.sleep(random.randint(25,35))
            #if len(htmlfile)<=12200:
                #print "finish at page: "+str(page)
                #break




    def writetoaiml (self):
        global out,count
        out.write("  <category>\n")
        out.write("    <pattern>")
        words=self.question.encode("utf-8")
        if not words.strip():
            return
        words=words.replace("&","&amp;")
        words=words.replace("<","&lt;")
        words=words.replace(">","&gt;")
        words=words.replace("'","&apos;")
        words=words.replace('"',"&quot;")
        out.write(words)
        out.write("</pattern>\n")
        out.write("    <template>\n")
        print self.question
        if len(self.answers)>1:
            out.write("      <random>\n")
            for x in self.answers:
                print x
                out.write("        <li>")
                words=x.encode("utf-8").replace("&","&amp;")
                words=words.replace("<","&lt;")
                words=words.replace(">","&gt;")
                words=words.replace("'","&apos;")
                words=words.replace('"',"&quot;")
                out.write(words)
                out.write("</li>\n")
                #count += 1
                out.write("      </random>\n")
        else:
            x=self.answer.encode("utf-8")
            print x
            words=x.replace("&","&amp;")
            words=words.replace("<","&lt;")
            words=words.replace(">","&gt;")
            words=words.replace("'","&apos;")
            words=words.replace('"',"&quot;")
        #charset=chardet.detect(words)["encoding"]
            out.write(words+'\n')
        out.write("    </template>\n")
        out.write("  </category>\n")
        out.flush()
        count += 1
        print count
        #self.content=set()


    def writetorawfile(self):
        if not self.question.strip():
            return
        out2.write("问题:\n"+self.question.encode("utf-8")+"\n")
        out2.write("关键词:\n"+self.keyword.encode("utf-8")+"\n")
        out2.write("答案:\n")
        i=1
        for x in self.answers:
            out2.write("最佳答案Top"+str(i)+":\n"+x.encode("utf-8")+'\n')
            i+=1

        out2.write("引用链接:\n"+self.cururl.encode("utf-8")+"\n")
        out2.write("######################################\n")
        out2.flush()

if __name__ == "__main__":
    zhihudm=zhihu()
    startpage=3
    endpage=10
    keyword="金融"
    answercount=3
    zhihudm.dealquestions(startpage,endpage,keyword,answercount)
