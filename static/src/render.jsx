var aesscript =  "/static/src/aesdecrypt.js";
var rc4script =  "/static/src/rc4decrypt.js";
var tdesscript =  "/static/src/tdesdecrypt.js";
var tjs = "text/javascript";
var Script = React.createClass({
    getInitialState: function () {
        return {scheme: ""}
    },
    changeText: function (event) {
        this.setState(
            {scheme: event.target.value}
        )
    },
    renderAES: function () {
        return (
            <div>
                <input id="encryption_schema" type="text" placeholder="AES / TripleDES / RC4" value={this.state.scheme} onChange={this.changeText}/>
                <h1 id="encryption_heading">AES Decryption using CryptoJS</h1>
                <div>
                    Key (64 hexadecimal characters)
                </div>
                <div>
                    <input id='key' type='text' size="61" placeholder="0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff"/>
                </div>
                <div>
                    IV (32 hexadecimal characters)
                </div>
                <div>
                    <input id='iv' type='text' size="30" placeholder="0123456789abcdeffedcba987654321"/>
                </div>
            </div>
        )
    },
    renderTripleDES: function () {
        return  (
            <div>
                <input id="encryption_schema" type="text" placeholder="AES / TripleDES / RC4" value={this.state.scheme} onChange={this.changeText}/>
                <h1 id="encryption_heading">TripleDES Decryption using CryptoJS</h1>
                <div>
                    Key (48 hexadecimal characters)
                </div>
                <div>
                    <input id='key' type='text' size="46" placeholder="000111222333444555666777888999aaabbbcccdddeeefff"/>
                </div>
                <div>
                    IV (16 hexadecimal characters)
                </div>
                <div>
                    <input id='iv' type='text' size="15" placeholder="0123456789abcdef"/>
                </div>
            </div>
        )
    },
    renderRC4: function () {
        return(
            <div>
                <input id="encryption_schema" type="text" placeholder="AES / TripleDES / RC4" value={this.state.scheme} onChange={this.changeText}/>
                <h1 id="encryption_heading">RC4 Decryption using CryptoJS</h1>
                <div>
                    Key (32 hexadecimal characters)
                </div>
                <div>
                    <input id='key' type='text' size="46" placeholder="0123456789abcdeffedcba9876543210"/>
                </div>
            </div>
        )
    },
    render: function () {
        if(this.state.scheme==="AES") {
            return this.renderAES()
        }
        else if(this.state.scheme==="TripleDES") {
            return this.renderTripleDES()
        }
        else if(this.state.scheme==="RC4"){
            return this.renderRC4()
        }
        else {
            return (
                <div>
                    <input id="encryption_schema" type="text" placeholder="AES / TripleDES / RC4" value={this.state.scheme} onChange={this.changeText}/>
                    <div>Please choose a schema, decrypt wouldn't work otherwise</div>
                </div>
            )
        }
    }
});

ReactDOM.render(
    <Script/>,
    document.getElementById("decryption_div")
);
