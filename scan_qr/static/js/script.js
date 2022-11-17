const capture         = document.querySelector(".button-64")
const video           = document.getElementById("video")
const videoScannerImg = document.querySelector(".video")
const border          = document.querySelector(".border")
const requests = new XMLHttpRequest();
const url = "/check_qr"

let canvas = document.querySelector("#canvas");
let Img;

var devices = []

navigator.mediaDevices.enumerateDevices()
    .then(gotDevices)
    .catch(function error(errorCallback){
      console.log(errorCallback.messageText)
    })

function gotDevices(deviceInfos) {



    for (var i = 0; i !== deviceInfos.length; ++i) {
      var deviceInfo = deviceInfos[i];
      if (deviceInfo.kind == "videoinput"){
        var deviceIds = deviceInfo.deviceId
        devices.push(deviceIds) //this will putn all video input devices on an array
      }
    }
    
}


video.addEventListener("click",()=> {
    startCam()
})

const startCam = () => {
    hide()
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video:
           {deviceId:{exact:devices[1]}}
        })
        // i choosed video output 1 for my phone front end camera, u can always change it to 0 if it doesn't work for u at first place
        .then((stream) => {
          video.srcObject = stream;
        })
        .catch(function (error) {
          console.log("Something went wrong!");
        });
    }
  };
  
function hide() {
    videoScannerImg.style.display = "none"
    video.style.display = "block"
    border.style.position = "relative"
    border.style.backgroundImage = "url()"
}


capture.addEventListener("click",()=> {
        canvas.classList.add("animateCanvas");
        canvas.style.zIndex = 1000
        canvas.getContext('2d').drawImage(video,0,0,canvas.clientHeight,canvas.clientWidth);
        //document.write(canvas.clientHeight,canvas.clientWidth)
        let image_data_url =  canvas.toDataURL('image/jpeg');
        let date = new Date
   	    console.log({
            "Generated_at":date.toISOString(),
            image_data_url
        });
        Img = {
            "Generated_at":date.toISOString(),
            image_data_url
    }
    console.log(navigator.mediaDevices.enumerateDevices())
    makeRequest(image_data_url)
    remove()
})

function makeRequest(data){
  requests.open("POST",url);
  requests.send(JSON.stringify({
    image : data
  }))
  requests.onreadystatechange = (e) => {
    if (requests.responseText == "1"){
      document.getElementById("response").innerHTML = "Successful ! Member of CCNA"
    }
    else{
      document.getElementById("response").innerHTML = "Unsuccessful ! He ain't registered !"
    }
  }
}

function remove() {
    setTimeout(() => {
        canvas.classList.remove("animateCanvas")
        canvas.style.zIndex = "-1"
    }, 700);
}
