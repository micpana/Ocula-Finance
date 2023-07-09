import React, { Component } from 'react';
import './App.css';
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from 'react-router-dom';
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import PageNotFound from './components/page_not_found'
import Signup from './components/signup'
import Signin from './components/signin'
import EmailVerificationSent from './components/email_verification_sent'
import VerifyEmail from './components/verify_email'
import ForgotPassword from './components/forgot_password'
import NewPasswordOnRecovery from './components/new_password_on_recovery'
import Dashboard from './components/dashboard'

class App extends Component {
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            
        };
    }

    componentDidMount() {

    }

    render() {
        return (
        <div className="App" style={{}}>
            <BrowserRouter>
                <Routes>
                    <Route path='/' element={<Signin />}/>
                    <Route path='/email-verification-sent/account_id' element={<EmailVerificationSent />}/>
                    <Route path='/verify-email/:verification_token' element={<VerifyEmail />}/>
                    <Route path='/forgot-password' element={<ForgotPassword />}/>
                    <Route path='/new-password-on-recovery/:recovery_token' element={<NewPasswordOnRecovery />}/>
                    <Route path='/signup' element={<Signup />}/>
                    <Route path='/dashboard' element={<Dashboard />}/>
                    <Route path="*" element={<PageNotFound />} />
                </Routes>
            </BrowserRouter>    
        </div>
        );
    }
}

export default withCookies(App);