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
import NavBar from './components/navbar';
import Footer from './components/footer';
import PageNotFound from './components/page_not_found'
import Home from './components/home'
import HowItWorks from './components/how_it_works'
import Pricing from './components/pricing'
import AboutUs from './components/about_us'
import ContactUs from './components/contact_us'
import AIPerformance from './components/ai_performance'
import Signup from './components/signup'
import Signin from './components/signin'
import EmailVerificationSent from './components/email_verification_sent'
import VerifyEmail from './components/verify_email'
import ForgotPassword from './components/forgot_password'
import NewPasswordOnRecovery from './components/new_password_on_recovery'
import Dashboard from './components/dashboard'
import TermsOfService from './components/terms_of_service'
import PrivacyPolicy from './components/privacy_policy'

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
        <div className="App" style={{backgroundColor: '#FAFAFA', color: '#383838'}}>
            <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path='/' element={<Home />}/>
                    <Route path='/how-it-works' element={<HowItWorks />}/>
                    <Route path='/pricing' element={<Pricing />}/>
                    <Route path='/about-us' element={<AboutUs />}/>
                    <Route path='/contact-us' element={<ContactUs />}/>
                    <Route path='/ai-performance' element={<AIPerformance />}/>
                    <Route path='/email-verification-sent/:account_id' element={<EmailVerificationSent />}/>
                    <Route path='/verify-email/:verification_token' element={<VerifyEmail />}/>
                    <Route path='/forgot-password' element={<ForgotPassword />}/>
                    <Route path='/new-password-on-recovery/:recovery_token' element={<NewPasswordOnRecovery />}/>
                    <Route path='/signup' element={<Signup />}/>
                    <Route path='/signin' element={<Signin />}/>
                    <Route path='/terms-of-service' element={<TermsOfService />}/>
                    <Route path='/privacy-policy' element={<PrivacyPolicy />}/>
                    <Route path='/dashboard' element={<Dashboard />}/>
                    <Route path="*" element={<PageNotFound />} />
                </Routes>
                <Footer />
            </BrowserRouter>    
        </div>
        );
    }
}

export default withCookies(App);