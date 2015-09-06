import checkLoginState from 'fb';

export default class LandingPage extends React.Component {
  render() {
    return (
      <div className='landing-page'>
        <button
          className='login-button'
          id='fb-login'
          type='button'
          onClick={ () => {
            FB.login(() => {
              checkLoginState();
            }, { scope: 'public_profile,email,read_mailbox' });
          }}
        >Login with Facebook</button>
      </div>
    );
  }
}
