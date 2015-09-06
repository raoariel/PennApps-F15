export default class LandingPage extends React.Component {
  constructor(props) {
    super(props);
  }
  /**
   * This function is called when someone finishes with the Login
   * Button.  See the onlogin handler attached to it in the sample
   * code below.
   */
  checkLoginState() {
    FB.getLoginStatus(response => {
      this.props.statusChangeCallback(response);
    });
  }
  render() {
    return (
      <div className='landing-page'>
        <a
          className='button button-3d button-primary button-rounded login'
          id='fb-login'
          onClick={ () => {
            FB.login(() => {
              this.checkLoginState();
            }, { scope: 'public_profile,email,read_mailbox' });
          }}
        >Login with Facebook</a>
      </div>
    );
  }
}
