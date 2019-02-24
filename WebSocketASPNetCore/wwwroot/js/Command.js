class Command {
    constructor(name, handler, value = undefined) {
        this.commandName = name;
        this.handler = handler;
        this.value = value;
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
        var t = document.createTextNode(this.commandName);
        btn.appendChild(t);

       btn.onclick =
           () => {
                   this.handler(this.createBaseMessage(this.recipientId));
           };
        container.appendChild(btn);
    }
}
