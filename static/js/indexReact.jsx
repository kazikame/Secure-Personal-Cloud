// first creating the main component, a file icon, i guess

var File = React.createClass({
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
    <File/>,
    document.getElementById('list_of_files')
);
