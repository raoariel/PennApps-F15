export default class LandingPage extends React.Component {
  /**
   * This function is called when someone finishes with the Login
   * Button.  See the onlogin handler attached to it in the sample
   * code below.
   */
  checkLoginState() {
    FB.getLoginStatus(function(response) {
      this.props.statusChangeCallback(response);
    });
  }
  render() {
    return (
      <div className='landing-page'>
        <button
          id='fb-login'
          type='button'
          onClick={ () => {
            FB.login(() => {
              this.checkLoginState();
            }, { scope: 'public_profile,email,read_mailbox' });
          }}
        >Login with Facebook</button>
      </div>
    );
  }
}
