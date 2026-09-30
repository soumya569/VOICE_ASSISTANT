$(document).ready(function () {

    // 1. Display Animated Status Message
    eel.expose(DisplayMessage);
    function DisplayMessage(message) {
        if (!message) return;
        
        // Update hidden text list element
        $(".siri-message .texts li").text(message);

        // Re-trigger textillate CSS3 animation
        try {
            $('.siri-message').textillate('start');
        } catch (e) {
            $('.siri-message').text(message);
        }
    }

    // 2. Display Static Sphere (Hide Active Waves)
    eel.expose(ShowHood);
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    // 3. Append User Message to Chat UI
    eel.expose(senderText);
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (chatBox && message && message.trim() !== "") {
            // Escape special HTML characters to prevent breaking layout
            var safeMessage = $("<div>").text(message).html();

            var messageRow = `
                <div class="row justify-content-end mb-4">
                    <div class="width-size">
                        <div class="sender_message">${safeMessage}</div>
                    </div>
                </div>`;
            
            chatBox.innerHTML += messageRow;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // 4. Append Assistant Response to Chat UI
    eel.expose(receiverText);
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (chatBox && message && message.trim() !== "") {
            var safeMessage = $("<div>").text(message).html();

            var messageRow = `
                <div class="row justify-content-start mb-4">
                    <div class="width-size">
                        <div class="receiver_message">${safeMessage}</div>
                    </div>
                </div>`;
            
            chatBox.innerHTML += messageRow;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // 5. Auth & Startup Animation Transitions
    eel.expose(hideLoader);
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);
    }

    eel.expose(hideFaceAuth);
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }

    eel.expose(hideFaceAuthSuccess);
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);
    }

    eel.expose(hideStart);
    function hideStart() {
        $("#Start").attr("hidden", true);

        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");
        }, 1000);

        setTimeout(function () {
            $("#Oval").attr("hidden", false);
        }, 1000);
    }

});