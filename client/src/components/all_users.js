import React, { Component, useReducer } from 'react';
import {
    Collapse, 
    Table, 
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

class AllUsers extends Component{
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) { 
        super(props);
        this.state = {
            loading: false,
            input_errors: {},
            on_mobile: false,
            screen: 'users', // users / user
            all_users: [
                {
                    firstname: 'Michael',
                    lastname: 'Mudimbu',
                    username: 'micpana',
                    email: 'michaelmudimbu@gmail.com',
                    phonenumber: '+263782464219',
                    country: 'Zimbabwe',
                    date_of_registration: '14/10/2023 11:15am',
                    verified: true,
                    subscribed: true,
                    subscription_date: '14/10/2023 11:15am',
                    subscription_expiry: '14/11/2023 11:15am',
                    role: 'admin',
                    banned: false
                }
            ],
            user: null
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

        this.GetAllUsers = () => {
            const { cookies } = this.props;
            this.setState({loading: true})

            axios.post(Backend_Server_Address + 'getAllUsers', null, { headers: { 'access_token': cookies.get(Access_Token_Cookie_Name) }  })
            .then((res) => {
                let result = res.data
                // set users to state
                this.setState({all_users: result, loading: false})
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
                this.setState({loading: false})
            })
        }
    }

    Notification = (message, message_type) => { // message type -> info / success / warning / error
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

    componentDidMount() {
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
            this.setState({
                on_mobile: true
            })
        }
        // this.GetAllUsers()
    }

    render() {
        // active screen
        var screen = this.state.screen
        // users
        var all_users = this.state.all_users
        var all_users_map = all_users.map((item, index) => {
            return <tr onClick={() => this.setState({user: item, screen: 'user'})}
                style={{borderBottom: '1px solid silver', cursor: 'pointer'}}
            >
                <td>{item.firstname}</td>
                <td>{item.lastname}</td>
                <td>{item.username}</td>
                <td>{item.email}</td>
            </tr>
        })
        // user
        var user = this.state.user

        return (
            <div>
                <Helmet>
                    <title>All Users | {Platform_Name}</title>
                    {/* <meta name="description" content="" /> */}
                </Helmet>
                {
                    this.state.loading === true
                    ? <LoadingScreen />
                    : <div>
                        <br/>
                        <h5 style={{fontWeight: 'bold'}}>
                            All Users
                        </h5>
                        <br/><br/>
                        {
                            screen === 'users'
                            ? <>
                                <div style={{maxHeight: '450px', overflowY: 'scroll'}}>
                                    <Table>
                                        <thead>
                                            <tr style={{borderBottom: '1px solid silver'}}>
                                                <th width='25%'>Firstname</th>
                                                <th width='25%'>Lastname</th>
                                                <th width='25%'>Username</th>
                                                <th width='25%'>Email</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {all_users_map}
                                        </tbody>
                                    </Table>
                                </div>
                            </>
                            : screen === 'user'
                            ? <>
                                <div style={{textAlign: 'left'}}>
                                    <Button onClick={() => this.setState({screen: 'users', user: null})}
                                        style={{border: '1px solid #00539C', borderRadius: '20px', color: '#ffffff', fontWeight: 'bold', backgroundColor: '#00539C', width: '180px'}}
                                    >
                                        {'<<<'} Back
                                    </Button>
                                </div>
                                <br/><br/>
                                <Row style={{margin: '0px'}}>
                                    <Col sm='6'>
                                        <div style={{border: '1px solid grey', borderRadius: '20px', minHeight: '100px'}}>
                                            <br/>
                                            <h6 style={{fontWeight: 'bold', color: '#00539C'}}>
                                                User Information
                                            </h6>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Firstname:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.firstname}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Lastname:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.lastname}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Username:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.username}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Email:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.email}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Phonenumber:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.phonenumber}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Country:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.country}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Date of registration:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.date_of_registration}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Verified:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {
                                                        user.verified === true
                                                        ? <>Yes</>
                                                        : <>No</>
                                                    }
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Subscribed:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {
                                                        user.subscribed === true
                                                        ? <>Yes</>
                                                        : <>No</>
                                                    }
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Subscription Date:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.subscription_date}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Subscription Expiry:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.subscription_expiry}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Account type:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {user.role}
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                            <Row style={{margin: '0px', textAlign: 'left'}}>
                                                <Col xs='6' style={{fontWeight: 'bold'}}>
                                                    Banned:
                                                    <br/>
                                                </Col>
                                                <Col>
                                                    {
                                                        user.banned === true
                                                        ? <>Yes</>
                                                        : <>No</>
                                                    }
                                                    <br/>
                                                </Col>
                                            </Row>
                                            <br/>
                                        </div>
                                    </Col>
                                    <Col>
                                    
                                    </Col>
                                </Row>
                            </>
                            : <>
                                <br/><br/><br/>
                                <h5 style={{color: '#005fc9'}}>Something went wrong.</h5>
                                <br/><br/><br/>
                                <Grid width='180px' style={{color: '#005fc9'}}/>
                            </>
                        }
                    </div>
                }
            </div>
        );
    }

};

export default withCookies(AllUsers);