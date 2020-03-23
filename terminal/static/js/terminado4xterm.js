// Copyright (c) Jupyter Development Team
// Copyright (c) 2014, Ramalingam Saravanan <sarava@sarava.net>
// Distributed under the terms of the Simplified BSD License.

function make_terminal(element, size, ws_url) {
    var ws = new WebSocket(ws_url);
    var term = new Terminal({
        cols: size.cols,
        rows: size.rows - 15,
        screenKeys: true,
        useStyle: true
    });
    ws.onopen = function (event) {
        ws.send(JSON.stringify(["set_size", size.rows, size.cols,
            window.innerHeight, window.innerWidth]));


        term.onData(function (data) {
            ws.send(JSON.stringify(['stdin', data]));
        });


        term.onTitleChange(function (title) {
            document.title = title;
        });


        term.onTitleChange = function (title) {
            document.title = title;
        };

        term.open(element);

        ws.onmessage = function (event) {
            json_msg = JSON.parse(event.data);
            console.log("get json_msg")
            console.log(json_msg)
            switch (json_msg[0]) {
                case "stdout":
                    term.write(json_msg[1]);
                    break;
                case "disconnect":
                    term.write("\r\n\r\n[Finished... Terminado]\r\n");
                    break;
            }
        };
    };
    return {socket: ws, term: term};
}