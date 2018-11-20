// first creating the main component, a file icon, i guess

var FileIcon = React.createClass({
    getInitialState: function() {
        return {customText: ""}
    },
    fileClicked: function() {
        alert('File clicked');
        this.setState({customText: "you clicked!"})
    },
    render: function () {
        return (
            <div>
                Fuck off!
            </div>
        )

    }
});

ReactDOM.render(
    <FileIcon/>,
    document.getElementById('list_of_files')
);
