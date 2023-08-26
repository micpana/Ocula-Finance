import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupAddon,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import { withCookies, Cookies } from 'react-cookie';
import { instanceOf } from 'prop-types';
import { Helmet } from 'react-helmet'
import {
    Audio,
    BallTriangle,
    Bars,
    Circles,
    Grid,
    Hearts,
    Oval,
    Puff,
    Rings,
    SpinningCircles,
    TailSpin,
    ThreeDots,
} from '@agney/react-loading';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import { Message, useToaster } from "rsuite";
import AboutUs1 from '../images/about_us_1.svg'
import AboutUs2 from '../images/about_us_2.svg'
import AboutUs3 from '../images/about_us_3.svg'
import AboutUs4 from '../images/about_us_4.svg'
import AboutUs5 from '../images/about_us_5.svg'

class AboutUs extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {}
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // if field error state doesn't already exist
            if (this.state.input_errors[field] == undefined){
                // new error
                var new_error = {
                    [field]: error
                }

                // existing errors + new
                var updated_input_errors = {
                    ...this.state.input_errors,
                    ...new_error
                }

                // update state
                this.setState({input_errors: updated_input_errors})
            }else{ // field error state already exists
                // existing errors
                var existing_errors = this.state.input_errors

                // existing errors modified
                existing_errors[field] = error

                // update state
                this.setState({input_errors: existing_errors})
            }
        }

        this.ClearInputErrors = () => {
            this.setState({input_errors: {}})
        }

        this.Notification = (message, message_type) => { // message type -> info / success / warning / error
            const toaster = useToaster();
            
            // push notification message
            toaster.push(<Message>{message}</Message>, {
                placement: 'topCenter',
                closable: true,
                type: message_type,
                showIcon: true,
                duration: 15000
            });
        }
    }

    componentDidMount() {
        
    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>About Us | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <Container>
                        <br/><br/><br/>
                        <h4 style={{fontWeight: 'bold'}}>
                            About us
                        </h4>
                        <br/><br/>
                        <img src={AboutUs1} style={{width: '100%'}}/>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Welcome to {Platform_Name} - Your Intelligence Partner for Forex Trading. We leverage Artificial 
                            Intelligence to provide deep analysis of the financial markets, particularly focusing on the Forex 
                            markets.
                        </p>
                        <br/><br/><br/>
                        <img src={AboutUs2} style={{width: '100%'}}/>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Our SAAS platform employs sophisticated AI models to predict potential upmoves and downmoves in the 
                            market over the next 105 minutes. These forecasts are updated every 15 minutes and are designed to 
                            equip traders with a risk-reward profile for informed trading decisions.
                        </p>
                        <br/><br/><br/>
                        <img src={AboutUs3} style={{width: '100%'}}/>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Taking a cue from established statistical models used in financial markets such as VaR and ER, we’ve 
                            upped the game by implementing deep neural networks. This approach provides more precision in 
                            predicting the potential percentages to be moved in any direction.
                        </p>
                        <br/><br/><br/>
                        <img src={AboutUs4} style={{width: '100%'}}/>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Whether you're deciding to use these metrics as sole guides, or you're integrating them with existing 
                            trading strategies, our goal remains the same - to simplify complex data and provide powerful metrics. 
                            Our vision is to aid traders in minimizing risk and maximizing rewards, all in an affordable manner.
                        </p>
                        <br/><br/><br/>
                        <img src={AboutUs5} style={{width: '100%'}}/>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Join {Platform_Name} today and optimize your Forex Trading with the ultimate support of AI-powered 
                            analysis. We believe that technology and analytics should be affordable, simple, and impactful, 
                            offering each of our users more control over their trades. Welcome to the future of Forex Trading.
                        </p>
                        <br/><br/><br/>
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(AboutUs);