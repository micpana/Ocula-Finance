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
import { ToastContainer, toast } from 'react-toastify';
import { Platform_Name } from '../platform_name';
import { Backend_Server_Address } from '../backend_server_url';
import { Access_Token_Cookie_Name } from '../access_token_cookie_name';
import axios from 'axios';
import { Unknown_Non_2xx_Message, Network_Error_Message, No_Network_Access_Message } from '../network_error_messages';
import LoadingScreen from './loading_screen';
import InputErrors from './input_errors';
import Notification from './notification_alert';
import NetworkErrorScreen from './network_error_screen';
import Analysis from './analysis'
import Subscriptions from './subscriptions'
import PastPayments from './past_payments'
import Settings from './settings'
import AllUsers from './all_users'
import UserCountryRanking from './user_country_ranking'
import NewUserRegistrationChart from './new_user_registation_chart'
import NewUserSubscriptionChart from './new_user_subscription_chart'
import UserCountChart from './user_count_chart'
import SubscribedUsersChart from './subscribed_users_chart'
import EarningsReport from './earnings_report'
import PaymentsList from './payments_list';
import { FaChartLine, FaUserPlus, FaMoneyCheckAlt, FaCogs, FaUsers, FaFlag, FaChartBar, FaRegChartBar, FaUserFriends, FaUserCheck, FaCoins, FaCashRegister } from 'react-icons/fa';

class Dashboard extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: true,
            network_error_screen: false,
            network_error_message: '',
            retry_function: null,
            input_errors: {},
            on_mobile: false,
            screen: 'analysis', // analysis / subscriptions / past payments / settings / all users / user country ranking / user registration chart / user subscription chart
            user_details: null
        };

        this.HandleChange = (e) => {
            this.setState({[e.target.name]: e.target.value});
        };

        this.SetInputError = (field, error) => { // error -> required / invalid
            // existing errors
            var existing_errors = this.state.input_errors

            // existing errors modified
            existing_errors[field] = error

            // update state
            this.setState({input_errors: existing_errors})
        }

        this.ClearInputErrors = () => {
            // existing errors
            var existing_errors = this.state.input_errors
            // array of existing error field names
            var existing_error_fields = Object.keys(existing_errors)
            // set existing error fields to undefined, clearing them
            existing_error_fields.map((item, index) => {
                existing_errors[item] = undefined
            })
            this.setState({input_errors: existing_errors})
        }

        this.LoadingOn = () => {
            this.setState({loading: true})
        }

        this.LoadingOff = () => {
            this.setState({loading: false})
        }

        this.NetworkErrorScreenOn = (error_message, retry_function) => {
            this.setState({network_error_screen: true, network_error_message: error_message, retry_function: retry_function})
        }

        this.NetworkErrorScreenOff = () => {
            this.setState({network_error_screen: false, network_error_message: '', retry_function: null})
        }

        this.CheckAccessTokenValidity = () => {
            const { cookies } = this.props;
            this.LoadingOn()
            this.NetworkErrorScreenOff()

            axios.post(Backend_Server_Address + 'getUserDetailsByAccessToken', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set user details to state
                this.setState({user_details: result})
                this.LoadingOff()
            }).catch((error) => {
                console.log(error)
                if (error.response){ // server responded with a non-2xx status code
                    let status_code = error.response.status
                    let result = error.response.data
                    var notification_message = ''
                    if(
                        result === 'access token disabled via signout' ||
                        result === 'access token expired' ||
                        result === 'not authorized to access this' ||
                        result === 'invalid token'
                    ){ 
                        // delete token from user cookies
                        // cookies.remove(Access_Token_Cookie_Name, { path: '/' });
                        // // redirect to sign in
                        // let port = (window.location.port ? ':' + window.location.port : '');
                        // window.location.href = '//' + window.location.hostname + port + '/signin';
                    }else{
                        notification_message = Unknown_Non_2xx_Message + ' (Error '+status_code.toString()+': '+result+')'
                        Notification(notification_message, 'error')
                        this.NetworkErrorScreenOn(notification_message, this.CheckAccessTokenValidity)
                    }
                }else if (error.request){ // request was made but no response was received ... network error
                    Notification(Network_Error_Message, 'error')
                    this.NetworkErrorScreenOn(Network_Error_Message, this.CheckAccessTokenValidity)
                }else{ // error occured during request setup ... no network access
                    Notification(No_Network_Access_Message, 'error')
                    this.NetworkErrorScreenOn(No_Network_Access_Message, this.CheckAccessTokenValidity)
                }
                this.LoadingOff()
            })
        }

        this.SwitchScreen = (e) => {
            // get current screen + selected screen
            const current_screen = this.state.screen
            const selected_screen = e.target.id

            // make button color highlight switch between current screen and selected screen
            document.getElementById(current_screen).style.color = '#ffffff'
            document.getElementById(selected_screen).style.color = '#F2B027'

            // switch screen to selected
            this.setState({screen: selected_screen})

            // scroll to screens container, for easy access on mobile
            document.getElementById('dashboard_screens_top').scrollIntoView()
        }
    }

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }

        // check access token existance
        const { cookies } = this.props;
        if(cookies.get(Access_Token_Cookie_Name) == null){
            let port = (window.location.port ? ':' + window.location.port : '');
            window.location.href = '//' + window.location.hostname + port + '/signin';
        }else{ 
            // check token's validity
            this.CheckAccessTokenValidity()
            // highlight current screen's button
            if (this.state.loading === false){
                document.getElementById(this.state.screen).style.color = '#F2B027'
            }
        }
    }

    render() {
        var screen = this.state.screen
        var user_role = this.state.user_details === null ? null : this.state.user_details.role

        return (
            <div>
                <Helmet>
                    <title>Dashboard | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                <ToastContainer />
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : this.state.network_error_screen === true
                    ? <NetworkErrorScreen error_message={this.state.network_error_message} retryFunction={this.state.retry_function} />
                    : <Row style={{margin: '0px'}}>
                        <Col sm='2' style={{minHeight: '550px', backgroundColor: '#00539C', color: '#ffffff'}}>
                            <br/>
                            <h6>
                                Dashboard
                            </h6>
                            <br/>
                            <Button id='analysis' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                            >
                                <FaChartLine id='analysis'/> Analysis
                            </Button>
                            <br/><br/>
                            <Button id='subscriptions' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                            >
                                <FaUserPlus id='subscriptions'/> Subscriptions
                            </Button>
                            <br/><br/>
                            <Button id='past payments' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                            >
                                <FaMoneyCheckAlt id='past payments'/> Past payments
                            </Button>
                            <br/><br/>
                            <Button id='settings' onClick={this.SwitchScreen} 
                                style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                            >
                                <FaCogs id='settings'/> Settings
                            </Button>
                            <br/><br/>
                            {
                                user_role === 'admin'
                                ? <div>
                                    <h6 style={{color: 'inherit', marginTop: '13px'}}>
                                        Admin Access
                                    </h6>
                                    <br/>
                                    <Button id='all users' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaUsers id='all users'/> All users
                                    </Button>
                                    <br/><br/>
                                    <Button id='user country ranking' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaFlag id='user country ranking'/> User country ranking
                                    </Button>
                                    <br/><br/>
                                    <Button id='user count chart' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaUserFriends id='user count chart'/> User count chart
                                    </Button>
                                    <br/><br/>
                                    <Button id='subscribed users chart' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaUserCheck id='subscribed users chart'/> Subscribed users chart
                                    </Button>
                                    <br/><br/>
                                    <Button id='new user registration chart' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaChartBar id='new user registration chart'/> New user registration chart
                                    </Button>
                                    <br/><br/>
                                    <Button id='new user subscription chart' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaRegChartBar id='new user subscription chart'/> New user subscription chart
                                    </Button>
                                    <br/><br/>
                                    <Button id='earnings report' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaCoins id='earnings report'/> Earnings report
                                    </Button>
                                    <br/><br/>
                                    <Button id='payments list' onClick={this.SwitchScreen} 
                                        style={{marginTop: '13px', backgroundColor: 'inherit', color: 'inherit', border: 'none', width: '100%', textAlign: 'left'}}
                                    >
                                        <FaCashRegister id='payments list'/> Payments list
                                    </Button>
                                    <br/><br/>
                                </div>
                                : <div></div>
                            }
                            <br/>
                        </Col>
                        <Col>
                            {/* div for scroll into view purposes upon screen selection */}
                            <div id='dashboard_screens_top' style={{minHeight: '150px', marginTop: '-150px', visibility: 'hidden'}}>

                            </div>
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
                                    : screen === 'user count chart'
                                    ? <UserCountChart />
                                    : screen === 'subscribed users chart'
                                    ? <SubscribedUsersChart />
                                    : screen === 'new user registration chart'
                                    ? <NewUserRegistrationChart />
                                    : screen === 'new user subscription chart'
                                    ? <NewUserSubscriptionChart />
                                    : screen === 'earnings report'
                                    ? <EarningsReport />
                                    : screen === 'payments list'
                                    ? <PaymentsList />
                                    : <div>
                                        <br/><br/><br/>
                                        <h5 style={{color: '#005fc9'}}>Something went wrong.</h5>
                                        <br/><br/><br/>
                                        <Grid width='180px' style={{color: '#005fc9'}}/>
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