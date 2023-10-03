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
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import { Message, useToaster } from "rsuite";

class Analysis extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            symbol: 'EURUSD',
            current_market_analysis: {},
            user_subscribed: null,
            symbols: [
                'EURUSD', 'GPBUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'USDZAR'
            ]
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

        this.GetCurrentMarketAnalysis = () => {
            const { cookies } = this.props;
            this.setState({loading: true})

            var data = new FormData()
            data.append('symbol', this.state.symbol)

            axios.post(Backend_Server_Address + 'getCurrentMarketAnalysis', data, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set current market analysis to state
                this.setState({current_market_analysis: result, loading: false})
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'Access token disabled via signout' ||
                        result === 'Access token expired' ||
                        result === 'Not authorized to access this' ||
                        result === 'Invalid token'
                    ){ 
                        // delete token from user cookies
                        cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // redirect to sign in
                        let port = (window.location.port ? ':' + window.location.port : '');
                        window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else if (result === 'not subscribed'){
                        this.setState({user_subscribed: false})
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        this.Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    this.Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    this.Notification(No_Network_Access_Message, 'error')
                }
                this.setState({loading: false})
            })
        }
    }

    componentDidMount() {
        this.GetCurrentMarketAnalysis()
    }

    render() {
        var current_market_analysis = this.state.current_market_analysis
        var maximum_possible_up_move = current_market_analysis.maximum_possible_up_move
        var maximum_possible_down_move = current_market_analysis.maximum_possible_down_move

        return (
            <div>
                <Helmet>
                    <title>Market Analysis | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <br/>
                        <h5 style={{fontWeight: 'bold'}}>
                            Analysis
                        </h5>
                        <br/><br/>
                        {
                            this.state.subscribed === false
                            ? <div>
                                <br/><br/><br/>
                                <h5 style={{color: '#005fc9'}}>You're not subscribed</h5>
                                <br/><br/><br/>
                                <Grid width='180px' style={{color: '#005fc9'}}/>
                            </div>
                            : <div>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='3'>
                                        <Label style={{fontWeight: 'bold'}}>Symbol:</Label>
                                        <select name='symbol' value={this.state.symbol} onChange={this.HandleChange}
                                            style={{border: 'none', width: '100%', backgroundColor: 'inherit', color: 'inherit', outline: 'none'}}
                                        >
                                            <option>Select a symbol for analysis</option>
                                            {
                                                this.state.symbols.map((item) => {
                                                    return<option value={item}>{item}</option>
                                                })
                                            }
                                        </select>
                                    </Col>
                                </Row>
                                <br/>
                                <Row style={{margin: '0px'}}>
                                    <h6 style={{fontWeight: 'bold'}}>Last updated:</h6> {current_market_analysis.timestamp}
                                </Row>
                                <br/>
                                <Row>
                                    <Col sm='6'>
                                        <Container>
                                            <div style={{backgroundColor: 'green', height: '150px', width: '150px', borderRadius: '50%'}}>
                                                <Container style={{paddingTop: '15px'}}>
                                                    <div style={{backgroundColor: '#FFFFFF', height: '120px', width: '120px', borderRadius: '50%'}}>
                                                        <h3 style={{'paddingTop': '30px'}}>
                                                            {maximum_possible_up_move} %
                                                        </h3>
                                                        <p>
                                                            Maximum possible up move
                                                        </p>
                                                    </div>
                                                </Container>
                                            </div>
                                        </Container>
                                        <br/>
                                    </Col>
                                    <Col sm='6'>
                                        <Container>
                                            <div style={{backgroundColor: 'red', height: '150px', width: '150px', borderRadius: '50%'}}>
                                                <Container style={{paddingTop: '15px'}}>
                                                    <div style={{backgroundColor: '#FFFFFF', height: '120px', width: '120px', borderRadius: '50%'}}>
                                                        <h3 style={{'paddingTop': '30px'}}>
                                                            {maximum_possible_down_move} %
                                                        </h3>
                                                        <p>
                                                            Maximum possible down move
                                                        </p>
                                                    </div>
                                                </Container>
                                            </div>
                                        </Container>
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='3' style={{fontWeight: 'bold', color: 'green'}}>
                                        Up-move risk-to-reward ratio:
                                        <br/>
                                    </Col>
                                    <Col>
                                        1:{Math.round((maximum_possible_up_move/maximum_possible_down_move) * 1000) / 1000}
                                        <br/>
                                    </Col>
                                </Row>
                                <br/>
                                <Row style={{margin: '0px', textAlign: 'left'}}>
                                    <Col sm='3' style={{fontWeight: 'bold', color: 'red'}}>
                                        Down-move risk-to-reward ratio:
                                        <br/>
                                    </Col>
                                    <Col>
                                        1:{Math.round((maximum_possible_down_move/maximum_possible_up_move) * 1000) / 1000}
                                        <br/>
                                    </Col>
                                </Row>
                            </div>
                        }
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(Analysis);