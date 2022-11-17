import smtplib,random,string,json,base64
from email.message import EmailMessage
from io import BytesIO
import qrcode
import queue
from threading import Thread
from email.utils import make_msgid

class CreateQrCode:
    """
        this method is used to create and send QR CODE Through Email for registered people on CCNA
            @file:str | a filepath or os.pathdir that contains all members needed
            @member:dict | informations about a registered member for CCNA {contains email, name, lastname}
    """
    def __init__(self,file:str) -> None:
        self.data = json.loads(open(file).read())
        self.email = open("email.html").read()
        self.smtp = ["smtp.gmail.com","587","email@gmail.com","somepassword"] # i am using gmail smtp; u can use any service
        self.newData = {
            "members":[]
        }

    def generateQR(self,member:dict):
        # member is a dict contains information about member
        uniqueStr = base64.b64encode("{0};{1}".format(member["name"],member["lastname"]).encode("utf-8")).decode("utf-8")
        self.newData["members"].append(uniqueStr)
        buffer = BytesIO()
        
        # creating qrcode and put it into buffer
 
        qrcode.make("{0};{1};{2}".format(member["name"],member["lastname"],uniqueStr)).save(buffer)
        buffer.seek(0)
        print("image created to {0} {1}".format(member["name"],member["lastname"]))
        self.sendMail(member["email"],buffer.read())

    def writeOutJson(self):
        content = json.dumps(self.newData,indent=4)
        file = open("registered.json","w+")
        file.write(content)
        file.close()
    
    def sendMail(self,member,image:bytes):
        server = smtplib.SMTP(self.smtp[0],self.smtp[1])
        server.ehlo()
        server.starttls()

        # setting up mime
        newContent = self.email # copy of the letter
        _,cid = self.imageembedded(member)
        newContent = newContent.replace("#IMAGE", str(cid["#IMAGE"])[1:-1])

        msg = EmailMessage()
        msg["From"] = self.smtp[2]
        msg["To"] = member
        msg.add_alternative(newContent,'html')
        msg = self.payloadImg(msg,image,cid)
        print(newContent)

        server.login(self.smtp[2],self.smtp[3])
        server.sendmail(msg["From"],member, msg.as_string())
        print("email sent to {}".format(member))
    
    def imageembedded(self,lead):
        cid = {}
        name_section = []
        try:
            image_cid = make_msgid(domain=lead.split("@")[1])
            name = "#IMAGE"
            cid[name] = image_cid

        except:
            pass
        return name_section,cid
    def payloadImg(self,msg,image,cid={}):
        mp = "#IMAGE"
        msg.get_payload()[0].add_related(image,
                                             maintype="image",
                                             subtype="png",
                                             cid=cid[mp])
        return msg

    def threadConfig(self,job):
        while not job.empty():
            member = job.get()
            try:
                self.generateQR(member)
            except Exception as e:
                print(e)
                print("couldn't send !")

def initThread(file:str):
    # use multi threads to fast up the process
    # @file is file's path

    creator = CreateQrCode(file=file)
    threadX = []
    job = queue.Queue()
    for member in creator.data["members"]:
        job.put(member)
    for i in range(5):
        thread = Thread(target = creator.threadConfig, args = (job,))
        thread.start()
        threadX.append(thread)
    for thread in threadX:
        thread.join()
    creator.writeOutJson()