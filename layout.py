_layoutHtml = """<!DOCTYPE html>
<html>
    <meta charset="utf-8">
    <head>
        <title>Cat house!</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #87CEEB; /* Sky color */
                overflow: hidden;
            }}
            
            .info {{
                position: absolute;
                left: 0;
                top: 0;
                padding: 20px;
                font-family: sans-serif;
                font-size: 40px;
            }}
            
            .info p {{
                background-color: #87CEEB;
            }}
            
            .scene {{
                position: relative;
                width: 100%;
                height: 100%;
            }}
            
            .sun {{
                position: absolute;
                top: 50px;
                right: 100px;
                width: 80px;
                height: 80px;
                background-color: #FFD700;
                border-radius: 50%;
                box-shadow: 0 0 50px #FFD700;
            }}
            
            .grass {{
                position: absolute;
                bottom: 0;
                width: 100%;
                height: 30%;
                background-color: #7CFC00;
            }}
            
            .house {{
                position: absolute;
                bottom: 30%;
                left: 50%;
                transform: translateX(-50%);
                width: 300px;
                height: 200px;
                background-color: #F0E68C;
            }}
            
            .roof {{
                position: absolute;
                top: -70px;
                left: -30px;
                width: 0;
                height: 0;
                border-left: 180px solid transparent;
                border-right: 180px solid transparent;
                border-bottom: 70px solid #8B4513;
            }}
            
            .door {{
                position: absolute;
                bottom: 0;
                left: 120px;
                width: 60px;
                height: 100px;
                background-color: #8B4513;
            }}
            
            .window {{
                position: absolute;
                width: 60px;
                height: 60px;
                background-color: #87CEEB;
                border: 2px solid #000;
            }}
            
            .window-left {{
                top: 65px;
                left: 30px;
            }}
            
            .window-right {{
                top: 65px;
                right: 30px;
            }}
            
            .cat {{
                position: absolute;
                bottom: 30%;
                right: 20%;
                width: 60px;
                height: 40px;
                background-color: #808080;
                border-radius: 50% 50% 0 0;
            }}
            
            .cat::before {{
                content: '';
                position: absolute;
                top: -15px;
                left: 10px;
                width: 30px;
                height: 30px;
                background-color: #808080;
                border-radius: 50%;
            }}
            
            .cat::after {{
                content: '';
                position: absolute;
                top: 5px;
                right: -5px;
                width: 10px;
                height: 20px;
                background-color: #808080;
                border-radius: 0 50% 50% 0;
            }}
        </style>
    </head>
    <body>
        <div class="info">
            <h1>Cat house! ₍^. .^₎⟆</h1>
            <p>{} is {}!</p>
            <p>Temperature inside: {:.1f} ℃ ({:.1f} ℉)</p>
            <p>Humidity inside: {:.1f} %</p>
            <p>Heating pad temperature: {:.1f} ℃ ({:.1f} ℉)</p>
            <p>Pico internal temperature: {:.1f} ℃ ({:.1f} ℉)</p>
        </div>
        <div class="scene">
            <div class="sun"></div>
            <div class="grass"></div>
            <div class="house">
                <div class="roof"></div>
                <div class="door"></div>
                <div class="window window-left"></div>
                <div class="window window-right"></div>
            </div>
            <div class="cat"></div>
        </div>
    </body>
    <script type="text/javascript">
        setTimeout(function() {{ window.location = window.location; }}, 5000);
    </script>
</html>
"""


