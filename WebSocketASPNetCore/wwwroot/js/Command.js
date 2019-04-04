class Command {
    constructor(name, caption, handler, value = undefined, description=undefined) {
        this.commandName = name;
        this.handler = handler;
        this.value = value;
        this.description = description;
        this.caption = caption;
    }
    createBaseMessage(recepientId) {
        var obj = { Id: getMessageId(), MessageType: "Command", Name: this.commandName, Recipients: recepientId };
        if (this.value !== undefined) obj.value = this.value;
        return obj;
    }

    getMessageId() {
        return Date.now().toString();
    }

   createButton(container) {
       var btn = document.createElement("BUTTON");
       btn.title = this.description;
        var t = document.createTextNode(this.caption);
        btn.appendChild(t);

       btn.onclick =
           () => {
                   this.handler(this.createBaseMessage(this.recipientId));
           };
        container.appendChild(btn);
    }
}
