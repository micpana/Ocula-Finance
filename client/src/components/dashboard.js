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
import Analysis from './analysis'
import Subscriptions from './subscriptions'
import PastPayments from './past_payments'
import Settings from './settings'
import AllUsers from './all_users'
import UserCountryRanking from './user_country_ranking'
import UserRegistrationChart from './user_registation_chart'
import UserSubscriptionChart from './user_subscription_chart'
import { FaChartLine, FaUserPlus, FaMoneyCheckAlt, FaCogs, FaUsers, FaFlag, FaChartBar, FaRegChartBar } from 'react-icons/fa';

class Dashboard extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            screen: 'analysis', // analysis / subscriptions / past payments / settings / all users / user country ranking / user registration chart / user subscription chart
            user_details: null
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

        this.CheckAccessTokenValidity = () => {
            const { cookies } = this.props;
            this.setState({loading: true})

            axios.post(Backend_Server_Address + 'getUserDetailsByAccessToken', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set loading to false
                this.setState({loading: false})
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
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        this.Notification(notification_message, 'error')
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    this.Notification(Network_Error_Message, 'error')
                }else{ // error occured during request setup ... no network access
                    this.Notification(No_Network_Access_Message, 'error')
                }
                // this.setState({loading: false})
            })
        }

        this.SwitchScreen = (e) => {
            // get current screen + selected screen
            const current_screen = this.state.screen
            const selected_screen = e.target.id

            // make button color highlight switch between current screen and selected screen
            document.getElementById(current_screen).style.color = '#ffffff'
            document.getElementById(selected_screen).style.color = '#00539C'

            // switch screen to selected
            this.setState({screen: selected_screen})
        }
    }

    componentDidMount() {
        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) == null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/signin';
        }else{ 
            // check token's validity
            this.CheckAccessTokenValidity()
            // highlight current screen's button
            document.getElementById(this.state.selected_screen).style.color = '#F2B027'
        }
    }

    render() {
        var screen = this.state.screen
        var user_role = this.state.user_details === null ? null : user_details.role

        return (
            <div>
                <Helmet>
                    <title>Dashboard | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <Row style={{margin: '0px'}}>
                        <Col sm='2' style={{minHeight: '550px', backgroundColor: '#00539C', color: '#ffffff'}}>
                            <br/>
                            <h6>
                                Dashboard
                            </h6>
                            <br/>
                            <Button id='analysis' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                            >
                                <FaChartLine id='analysis'/> Analysis
                            </Button>
                            <br/><br/>
                            <Button id='subscriptions' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                            >
                                <FaUserPlus id='subscriptions'/> Subscriptions
                            </Button>
                            <br/><br/>
                            <Button id='past payments' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                            >
                                <FaMoneyCheckAlt id='past payments'/> Past payments
                            </Button>
                            <br/><br/>
                            <Button id='settings' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                            >
                                <FaCogs id='settings'/> Settings
                            </Button>
                            <br/><br/>
                            {
                                user_role === 'admin'
                                ? <div>
                                    <Button id='all users' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                                    >
                                        <FaUsers id='all users'/> All users
                                    </Button>
                                    <br/><br/>
                                    <Button id='user country ranking' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                                    >
                                        <FaFlag id='user country ranking'/> User country ranking
                                    </Button>
                                    <br/><br/>
                                    <Button id='user registration chart' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                                    >
                                        <FaChartBar id='user registration chart'/> User registration chart
                                    </Button>
                                    <br/><br/>
                                    <Button id='user subscription chart' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', fontSize: '18px', textAlign: 'left'}}
                                    >
                                        <FaRegChartBar id='user subscription chart'/> User subscription chart
                                    </Button>
                                    <br/><br/>
                                </div>
                                : <div></div>
                            }
                            <br/>
                        </Col>
                        <Col>
                            <Container>
                                {
                                    screen === 'analysis'
                                    ? <Analysis />
                                    : screen === 'subscriptions'
                                    ? <Subscriptions />
                                    : screen === 'past payments'
                                    ? <PastPayments />
                                    : screen === 'settings'
                                    ? <Settings />
                                    : screen === 'all users'
                                    ? <AllUsers />
                                    : screen === 'user country ranking'
                                    ? <UserCountryRanking />
                                    : screen === 'user registration chart'
                                    ? <UserRegistrationChart />
                                    : screen === 'user subscription chart'
                                    ? <UserSubscriptionChart />
                                    : <div>
                                        <br/>
                                        <h3 style={{marginTop: '150px'}}>
                                            An unknown error has occured
                                        </h3>
                                    </div>
                                }
                                <br/><br/><br/>
                            </Container>
                        </Col>
                    </Row>
                }
            </div>
        );
    }

};

export default withCookies(Dashboard);