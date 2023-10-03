import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
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
import Jumbotron1 from '../images/jumbotron_1.jpg'
import Home1 from '../images/home_1.jpg'
import Home2 from '../images/home_2.jpg'
import Home3 from '../images/home_3.jpg'

class Home extends Component{
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
                    <title>Home | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <Row style={{color: '#ffffff', height: '550px', margin: '0px'}}>
                            <div style={{height: '550px', overflow: 'hidden', backgroundColor: '#005fc9'}}>
                                <img src={Jumbotron1} style={{width: '110%', height: '160%', marginLeft: '-30px', opacity: 0.6}}/>
                            </div>
                            <Container style={{position: 'absolute', top: '120px',left: '10px'}}>
                                <h1 style={{color: '#ffffff', fontWeight: 'bold', marginTop: '100px', textAlign: 'left'}}>
                                    Maximize Your Trading Potential with AI-Driven Analysis
                                </h1>
                                <h3 style={{color: '#FEF6DF', marginTop: '50px', textAlign: 'left'}}>
                                    Unlock Profitable Trading Opportunities with Accurate Forecasts and Risk-to-Reward Profiles. 
                                </h3>
                                <Row style={{marginRight: '0px', marginTop: '70px', textAlign: 'left'}}>
                                    <Col sm='6'>
                                        <Button href='/signup' style={{backgroundColor: '#ffffff', color: '#005fc9', fontWeight: 'bold', border: 'none', width: '180px'}}>
                                            Get started
                                        </Button>
                                        <br/><br/>
                                    </Col>
                                </Row>
                            </Container>
                        </Row>
                        <Container>
                            <Row style={{margin: '0px', minHeight: '300px'}}>
                                <Col sm='6'>
                                    {
                                        this.state.on_mobile == true
                                        ? <><br/><br/></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                    <img src={Home1} style={{width: '100%', border: '1px solid #00539C', borderRadius: '10px'}} />
                                </Col>
                                <Col>
                                    {
                                        this.state.on_mobile == true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/><br/><br/><br/><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Analyze, Predict, and Profit.
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: "left"}}>
                                        {Platform_Name} is designed to deliver data-driven predictions on market movements for the 
                                        next 1hr 45min. Our revolutionary platform carefully examines the market dynamics 
                                        and provides you with a potential maximum up-move and down-move for this period.
                                    </p>
                                    {
                                        this.state.on_mobile == true
                                        ? <></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                </Col>
                            </Row>
                            <Row style={{margin: '0px', minHeight: '300px'}}>
                                {
                                    this.state.on_mobile == true
                                    ? <Col>
                                        <br/><br/>
                                        <img src={Home2} style={{width: '100%'}} />
                                    </Col>
                                    : <></>
                                }
                                <Col sm='6'>
                                    {
                                        this.state.on_mobile == true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/><br/><br/><br/><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Maximise Your Gains, Minimise Your Risks.
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: "left"}}>
                                        We help traders construct favourable risk-to-reward profiles, taking the guesswork out of 
                                        trading decisions. {Platform_Name} is an affordable, powerful tool that complements your 
                                        existing strategies to give you a well-rounded trading perspective.
                                    </p>
                                    {
                                        this.state.on_mobile == true
                                        ? <></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                </Col>
                                {
                                    this.state.on_mobile == false
                                    ? <Col>
                                        <img src={Home2} style={{width: '100%'}} />
                                    </Col>
                                    : <></>
                                }
                            </Row>
                            <Row style={{margin: '0px', minHeight: '300px'}}>
                                <Col sm='6'>
                                    {
                                        this.state.on_mobile == true
                                        ? <><br/><br/></>
                                        : <></>
                                    }
                                    <img src={Home3} style={{width: '100%'}} />
                                </Col>
                                <Col>
                                    {
                                        this.state.on_mobile == true
                                        ? <><br/><br/><br/></>
                                        : <><br/><br/><br/><br/><br/><br/><br/><br/></>
                                    }
                                    <h6 style={{fontWeight: 'bold'}}>
                                        Advanced Tools, Simplified Trading.
                                    </h6>
                                    <br/><br/>
                                    <p style={{textAlign: "left"}}>
                                        With an operational method akin to well-known statistical models such as VaR and ER, 
                                        {Platform_Name} stands apart by employing deep neural networks, simplifying complex data 
                                        into manageable metrics for traders. This strategic utilization of AI enables us to gauge 
                                        potential percentage movements in either direction with remarkable precision.
                                    </p>
                                    {
                                        this.state.on_mobile == true
                                        ? <></>
                                        : <><br/><br/><br/><br/></>
                                    }
                                </Col>
                            </Row>
                            {
                                this.state.on_mobile == true
                                ? <><br/><br/><br/></>
                                : <><br/><br/><br/><br/><br/><br/><br/><br/></>
                            }
                            <h6 style={{fontWeight: 'bold'}}>
                                Join {Platform_Name} Today.
                            </h6>
                            <br/><br/>
                            <p style={{textAlign: "left"}}>
                                Gain a competitive edge in the market with our affordable, AI-driven forex market analysis. 
                                Sign up now and experience the next-level of trading insight.
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
                    </div>
                }
                <br/><br/><br/>
            </div>
        );
    }

};

export default withCookies(Home);