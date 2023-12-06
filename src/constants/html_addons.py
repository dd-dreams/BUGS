"""
this file has all html tags that is needed to make the outputted html file more prettier
like centering the text and so on

"""

# start of html file
HTML_BASICS_START = """
<!DOCTYPE html>
<html>
    <body onload="speed = 100;">
"""

HTML_BASICS_END = """
    </body>
</html>
"""

CENTER_SMOOTH_TEXT_START = """
    <style>
        html {
            scroll-behavior: smooth;
        }
        div.center {
            text-align: center;
            font-size: 20px;
        }   
    </style>
    <pre>
    <div class="center">
"""

CENTER_TEXT_END = "</div></pre>"

AUTO_SCROLL_BUTTON = """
<button onclick="scrollpage()">Autoscroll this GODDAMN PAGE</button>
"""

AUTO_SCROLL_SCRIPT = """
<script>
document.addEventListener("keyup", function(event) {
    if (event.key === '+' && speed != 0) {speed -= 100;}
    else if (event.key === '-') {speed += 100;}
});
function scrollpage() {
    var i = 0;
    var page_len = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    function scroll() {
        currentPosition = document.documentElement.scrollTop;
        if (i < currentPosition || i > currentPosition) { i = currentPosition; }
        i += 5;
        window.scrollTo(0,i);
        if(i >= page_len){  return; }
        setTimeout(scroll, speed);
    }scroll();
}
</script>
"""
