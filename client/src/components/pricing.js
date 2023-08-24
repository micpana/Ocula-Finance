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

class Pricing extends Component{
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
                    <title>Pricing | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading == true
                    ? <LoadingScreen />
                    : <Container>
                        <br/><br/><br/>
                        <h4 style={{fontWeight: 'bold'}}>
                            Pricing
                        </h4>
                        <br/><br/>
                        <h5>Uncover the Value of {Platform_Name}</h5>
                        <br/>
                        <h6>Discover our affordable plan that positions your trading decisions for success.</h6>
                        <br/><br/>
                        <p style={{textAlign: 'left'}}>
                            Welcome to the {Platform_Name} pricing page. Our advanced AI-powered platform provides pivotal market 
                            information at cost-effective rates, empowering traders to enhance their trading strategy with 
                            decisive data. Analyzing mostly forex markets, our system details the potential max upmove and max 
                            downmove for the next 1 hour 45 minutes. This precious data creates a risk-reward profile, helping 
                            establish the most advantageous market direction.
                        </p>
                        <br/>
                        <p style={{textAlign: 'left'}}>
                            Our goal is to equip traders with a simple yet powerful tool in an affordable manner, and that’s 
                            reflected in our pricing structure. {Platform_Name}’s pricing is designed to accommodate traders of all 
                            scales - from budding enthusiasts to seasoned professionals. We have designed a straightforward and 
                            transparent pricing system that ensures you get the most out of your trading experience. We invite you 
                            to explore our versatile pricing options to find a plan that suits your trading needs best. 
                            Please note that all our pricing plans offer full access to our AI-driven forecasts and risk-to-reward 
                            profiles.
                        </p>
                        <br/><br/><br/>
                        <Row style={{margin: '0px'}}>
                            <Col sm='4'>
                                <Row style={{margin: '0px', minHeight: '178px', backgroundColor: '#F9F9F9', borderRadiusTopLeft: '10px', borderRadiusTopRight: '10px'}}>
                                    <Container style={{textAlign: 'left'}}>
                                        <br/><br/>
                                        <h6 style={{fontWeight: 'bolder'}}>
                                            FREE TRIAL
                                        </h6>
                                        <br/>
                                        <Row style={{margin: '0px'}}>
                                            <h3 style={{fontWeight: 'bold'}}>
                                                $ 0.00
                                            </h3>
                                            For only 14 days
                                        </Row>
                                        <br/><br/>
                                    </Container>
                                </Row>
                                <Row style={{margin: '0px', minHeight: '437px', backgroundColor: '#FCFCFC', borderRadiusBottomLeft: '10px', borderRadiusBottomRight: '10px'}}>
                                    <Container>
                                        <br/><br/>
                                        ✅ Potential max upmove and downmove forecasts
                                        <br/>
                                        ✅ Risk-to-reward profiles
                                        <br/>
                                        ✅ Regular updates every 15 minutes
                                        <br/>
                                        ✅ Customer support
                                        <br/>
                                        ✅ 
                                        <br/>
                                        ✅
                                        <br/><br/>
                                        <Button href=''
                                            style={{border: '1px solid #005fc9', borderRadius: '20px', backgroundColor: '#ffffff', color: 'inherit'}}
                                        >
                                            Subscribe now
                                        </Button>
                                        <br/><br/>
                                    </Container>
                                </Row>
                            </Col>
                            <Col sm='4'>
                                <Row style={{margin: '0px', minHeight: '178px', backgroundColor: '#005fc9', color: '#ffffff', borderRadiusTopLeft: '10px', borderRadiusTopRight: '10px'}}>
                                    <Container style={{textAlign: 'left'}}>
                                        <br/><br/>
                                        <h6 style={{fontWeight: 'bolder'}}>
                                            MONTHLY
                                        </h6>
                                        <br/>
                                        <Row style={{margin: '0px'}}>
                                            <h3 style={{fontWeight: 'bold'}}>
                                                $ 10.00
                                            </h3>
                                            /Month
                                        </Row>
                                        <br/><br/>
                                    </Container>
                                </Row>
                                <Row style={{margin: '0px', minHeight: '437px', backgroundColor: '#FCFCFC', borderRadiusBottomLeft: '10px', borderRadiusBottomRight: '10px'}}>
                                    <Container>
                                        <br/><br/>
                                        ✅ Potential max upmove and downmove forecasts
                                        <br/>
                                        ✅ Risk-to-reward profiles
                                        <br/>
                                        ✅ Regular updates every 15 minutes
                                        <br/>
                                        ✅ Customer support
                                        <br/>
                                        ✅ 
                                        <br/>
                                        ✅
                                        <br/><br/>
                                        <Button href=''
                                            style={{border: '1px solid #005fc9', borderRadius: '20px', backgroundColor: '#005fc9', color: '#ffffff'}}
                                        >
                                            Subscribe now
                                        </Button>
                                        <br/><br/>
                                    </Container>
                                </Row>
                            </Col>
                            <Col sm='4'>
                                <Row style={{margin: '0px', minHeight: '178px', backgroundColor: '#F9F9F9', borderRadiusTopLeft: '10px', borderRadiusTopRight: '10px'}}>
                                    <Container style={{textAlign: 'left'}}>
                                        <br/><br/>
                                        <h6 style={{fontWeight: 'bolder'}}>
                                            YEARLY
                                        </h6>
                                        <br/>
                                        <Row style={{margin: '0px'}}>
                                            <h3 style={{fontWeight: 'bold'}}>
                                                $ 96.00
                                            </h3>
                                            /Year
                                        </Row>
                                        <br/><br/>
                                    </Container>
                                </Row>
                                <Row style={{margin: '0px', minHeight: '437px', backgroundColor: '#FCFCFC', borderRadiusBottomLeft: '10px', borderRadiusBottomRight: '10px'}}>
                                    <Container>
                                        <br/><br/>
                                        ✅ Potential max upmove and downmove forecasts
                                        <br/>
                                        ✅ Risk-to-reward profiles
                                        <br/>
                                        ✅ Regular updates every 15 minutes
                                        <br/>
                                        ✅ Customer support
                                        <br/>
                                        ✅ 
                                        <br/>
                                        ✅
                                        <br/><br/>
                                        <Button href=''
                                            style={{border: '1px solid #005fc9', borderRadius: '20px', backgroundColor: '#ffffff', color: 'inherit'}}
                                        >
                                            Subscribe now
                                        </Button>
                                        <br/><br/>
                                    </Container>
                                </Row>
                            </Col>
                        </Row>
                    </Container>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(Pricing);