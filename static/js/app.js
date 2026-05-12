let sessionId = null;

async function sendMessage(){

    const input = document.getElementById("message");

    const message = input.value;

    if(!message) return;

    addMessage(message,"user");

    input.value = "";

    const botDiv = addMessage("","bot");

    const response = await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message,
            session_id:sessionId
        })

    });

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    while(true){

        const {done,value} = await reader.read();

        if(done) break;

        const chunk = decoder.decode(value);

        const lines = chunk.split("\n");

        for(const line of lines){

            if(line.trim() === "") continue;

            try{

                const data = JSON.parse(line);

                if(data.session_id){
                    sessionId = data.session_id;
                }

                if(data.content){
                    botDiv.textContent += data.content;
                }

            }catch(err){

                console.error(err);

            }
        }

        window.scrollTo(
            0,
            document.body.scrollHeight
        );
    }
}

function addMessage(text,type){

    const chat = document.getElementById("chat");

    const div = document.createElement("div");

    div.classList.add("message");

    div.classList.add(type);

    div.textContent = text;

    chat.appendChild(div);

    return div;
}

document
.getElementById("message")
.addEventListener("keypress",function(e){

    if(e.key==="Enter"){
        sendMessage();
    }

});
