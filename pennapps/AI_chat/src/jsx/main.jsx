import 'django';
import Homepage from 'Homepage';
import LandingPage from 'LandingPage';

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isLoggedIn: false };
  }
  componentDidMount() {
    window.fbAsyncInit = () => {
      FB.init({
        appId      : '446920808773734',
        cookie     : true,  // enable cookies to allow the server to access
                            // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.3' // use version 2.3
      });

      // Now that we've initialized the JavaScript SDK, we call
      // FB.getLoginStatus().  This function gets the state of the
      // person visiting this page and can return one of three states to
      // the callback you provide.  They can be:
      //
      // 1. Logged into your app ('connected')
      // 2. Logged into Facebook, but not your app ('not_authorized')
      // 3. Not logged into Facebook and can't tell if they are logged into
      //    your app or not.
      //
      // These three cases are handled in the callback function.

      FB.getLoginStatus(response => {
        this.statusChangeCallback(response);
      });
    };

    // Load the SDK asynchronously
    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
  }
  statusChangeCallback(statusResponse) {
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (statusResponse.status === 'connected') {
      // Logged into your app and Facebook.
      let data;
      FB.api('/me/inbox', response => {
        data = response;
      });
      FB.api('/me', response => {
        this.login();
        $.ajax({
          url: '/register',
          method: 'post',
          data: {
            email: response.email,
            first_name: response.first_name,
            last_name: response.last_name,
            messages: data,
            userId: response.id,
            accessToken: statusResponse.authResponse.accessToken,
          },
          dataType: 'text',
        });
      });
    } else if (statusResponse.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      this.logout();
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      this.logout();
    }
  }
  login() {
    this.setState({ isLoggedIn: true });
  }
  logout() {
    this.setState({ isLoggedIn: false });
  }
  render() {
    return (
      this.state.isLoggedIn ?
        <Homepage />
      :
        <LandingPage statusChangeCallback={ this.statusChangeCallback } />
    );
  }
}

React.render(<Main />, $('.main-body')[0]);
