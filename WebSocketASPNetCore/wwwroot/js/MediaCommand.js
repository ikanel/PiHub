class MediaCommand extends BlobCommand {
    constructor(name, handler) {
        super(name, handler, undefined, false);
        this.isStarted = false;
    }

    stopMediaRecorder() {
        if (!this.isStarted) {
            alert("Media recorder is not started");
            return;
        }
        this.mediaRecorder.stop();
        this.isStarted = false;
    }

    startMediaRecorder() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                this.isStarted = true;
                this.mediaRecorder = new MediaRecorder(stream);
                this.mediaRecorder.start();

                this.audioChunks = [];
                this.mediaRecorder.addEventListener("dataavailable",
                    event => {
                        this.audioChunks.push(event.data);
                    });

                this.mediaRecorder.addEventListener("stop",
                    () => {
                        const audioBlob = new Blob(this.audioChunks);
                        const audioUrl = URL.createObjectURL(audioBlob);
                        //console.log(audioUrl);
                        var reader = new FileReader();
                        reader.readAsDataURL(audioBlob);
                        reader.onloadend =  ()=> {
                            var base64data = reader.result;
                            var result = base64data.substring(base64data.indexOf("base64,") + 7);
                            var message = this.createBlobMessage(this.recipientId, "record.webm", result.length, result);
                            this.handler(message, audioUrl);
                        
                        };
                    });

            });
    };

    createButton(container) {
        var btn = document.createElement("BUTTON");
        var t = document.createTextNode("Record Audio");
        btn.appendChild(t);

        btn.onclick =
            () => {
                if (this.isStarted) {
                    btn.innerText = "Record Audio";
                    this.stopMediaRecorder();
                } else {
                    btn.innerText = "Stop Audio Recording";
                    this.startMediaRecorder();
                   
                }
            }
        container.appendChild(btn);
    }
}

