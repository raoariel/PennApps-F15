export default class Homepage extends React.Component {
  constructor(props) {
    super(props);
    this.state = { messages: [] }
  }
  componentWillReceiveProps() {
    console.log(this.props.userId);
    $.ajax({
      url: '/get_messages',
      method: 'get',
      data: { user_id: this.props.userId },
      success: response => {
        console.log('resp');
        this.setState({ messages: response });
      },
    });
  }
  render() {
    return (
      <div className='homepage'>
        <div className='friends'></div>
        <div className='chatBox'>{ this.state.messages }</div>
      </div>
    );
  }
}
