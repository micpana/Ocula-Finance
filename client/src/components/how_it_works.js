import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup,
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
import HowItWorks1 from '../images/how_it_works_1.svg'
import HowItWorks2 from '../images/how_it_works_2.svg'
import HowItWorks3 from '../images/how_it_works_3.svg'
import HowItWorks4 from '../images/how_it_works_4.svg'
import HowItWorks5 from '../images/how_it_works_5.svg'

class HowItWorks extends Component{
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
                    <title>How It Works | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading == true
                    ? <LoadingScreen />
                    : <Container>
                        <br/><br/><br/>
                        <h4 style={{fontWeight: 'bold'}}>
                            How it works
                        </h4>
                        <br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            Introduction
                        </h6>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Welcome to {Platform_Name} - the Advanced SAAS platform that revolutionizes the way you approach 
                            financial markets, primarily forex. Powered by cutting-edge AI and deep neural networks, our platform 
                            provides you with comprehensive forecast data for the next 105 minutes, enabling you to create a 
                            balanced risk-to-reward profile for favourable market directions. Here's how our system works.
                        </p>
                        <br/>
                        <img src={HowItWorks1} style={{width: '100%'}} />
                        <br/><br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            What We Offer
                        </h6>
                        <br/><br/>
                        <Row style={{margin: '0px'}}>
                            <Col sm='6'>
                                <p style={{textAlign: 'left'}}>
                                    <ul>
                                        <li>Potential max upmove and downmove forecasts.</li><br/>
                                        <li>Comprehensive risk-to-reward profile construction.</li><br/>
                                        <li>Enhanced support to existing trading strategies.</li><br/>
                                        <li>Simple, powerful metrics for savvy trading.</li><br/>
                                        <li>Regular updates every 15 minutes.</li><br/>
                                    </ul>
                                </p>
                            </Col>
                            <Col>
                                <img src={HowItWorks2} style={{width: '100%'}} />
                            </Col>
                        </Row>
                        <br/><br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            Our Distinct Approach 
                        </h6>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            While our process mirrors the statistical models employed in market finance, such as VaR and ER, we 
                            have a critical edge. {Platform_Name} leverages the power of deep neural networks to provide potential 
                            percentages moved in either direction. This crucial difference amplifies the effectiveness of our 
                            platform and the insight users gain. 
                        </p>
                        <br/>
                        <img src={HowItWorks3} style={{width: '100%'}} />
                        <br/><br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            Empower Your Trading 
                        </h6>
                        <br/><br/>
                        <Row style={{margin: '0px'}}>
                            <Col sm='6'>
                                <p style={{textAlign: 'left'}}>
                                    Whether you're a seasoned trading expert or a newcomer, our metrics can serve as your 
                                    standalone guide or efficiently supplement your existing trading strategy. We aim to minimize 
                                    trading risks while maximizing rewards, all at an affordable price point.
                                </p>
                            </Col>
                            <Col>
                                <img src={HowItWorks4} style={{width: '100%'}} />
                            </Col>
                        </Row>
                        <br/><br/><br/>
                        <h6 style={{fontWeight: 'bold'}}>
                            Stay updated 
                        </h6>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            At {Platform_Name}, we understand the dynamic nature of financial markets, which is why we update our 
                            data every 15 minutes. Stay in sync with the latest trends and make data-driven decisions on the go.
                        </p>
                        <br/>
                        <img src={HowItWorks5} style={{width: '100%'}} />
                        {
                            this.state.on_mobile == true
                            ? <><br/><br/><br/></>
                            : <><br/><br/><br/><br/><br/><br/><br/><br/></>
                        }
                        <h6 style={{fontWeight: 'bold'}}>
                            Explore {Platform_Name} today and redefine your trading experience. 
                        </h6>
                        <br/><br/>
                        <p style={{textAlign: "left"}}>
                            Sign up for a 14-day Free Trial now!
                        </p>
                        <Row style={{margin: '0px'}}>
                            <Col sm='4'></Col>
                            <Col sm='4'></Col>
                            <Col sm='4'></Col>
                            <Col sm='4'>
                                <Button href='/signup' style={{backgroundColor: '#ffffff', color: '#005fc9', fontWeight: 'bold', border: 'none', width: '180px'}}>
                                    Sign up
                                </Button>
                            </Col>
                        </Row>
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(HowItWorks);