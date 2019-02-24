class BlobCommand extends Command {
    constructor(name, handler) {
        super(name, handler, undefined);
      }

    createBlob(filename, size, content) {
        return { Name: filename, Size: size, Content: content };
    }
    createBlobMessage(recepientId, filename, size, content) {
        var message = this.createBaseMessage(recepientId);
        message.Blob = this.createBlob(filename, size, content);
        return message;
    }

    blobHandler(recepientId, filename, size, content) {
        var message = this.createBlobMessage(recepientId, filename, size, content);
        this.handler(message);
    }

    readTheBlob(files, recipientId) {
        var content;
        if (files === undefined) {
            console.error("files must not be null")
        }
        if (files.files.length === 0) {
            alert("You have to select the file");
        }
        var reader = new FileReader();
        var fileName = files.files[0].name.split('/').pop().split('\\').pop();
        reader.readAsDataURL(files.files[0]);
        reader.onload = () => {
            var result = reader.result;
            result = result.substring(result.indexOf("base64,") + 7);
            this.blobHandler(recipientId, fileName, result.length, result);
        };
        reader.onerror = function (error) {
            console.log('Error: ', error);
        };


    }
    createButton(container) {
        var btn = document.createElement("BUTTON");
        var t = document.createTextNode(this.commandName);
        btn.appendChild(t);

        btn.onclick =
            () => {
                this.readTheBlob(this.files, this.recipientId);
            };
        container.appendChild(btn);
    }
}
