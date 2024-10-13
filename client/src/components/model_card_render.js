// Modal.js
import React from 'react';
import {
    Collapse, 
    Nav, NavItem, NavLink, 
    UncontrolledDropdown, Dropdown, DropdownToggle, DropdownMenu, DropdownItem, 
    Input, InputGroup, InputGroupText,
    Button, Row, Col, Form, Container, Label
} from "reactstrap";
import { Model_Cards } from './model_cards'
import SymbolIconsRender from './symbol_icons_render';

const ModelCardRender = ({ symbol }) => {
    // symbol's model card
    var symbol_model_card = Model_Cards[symbol]

    // model card render
    return (
        <div>
            <h5>
                {symbol} AI Model's Performance Card <SymbolIconsRender symbol={symbol} />
            </h5>
            <div style={{width: '100%', borderBottom: '1px solid #F9C961'}}></div>
            <br/>
            <p style={{fontSize: '13px', textAlign: 'left'}}>
                All test trades were taken using a fixed risk-to-reward ratio and a fixed risk amount in dollars, risking a single dollar to gain two.
            </p>
            <br/><br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Initial account balance:
                </Col>
                <Col>
                    ${symbol_model_card["Starting account balance (example in $)"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Account balance after test trades:
                </Col>
                <Col>
                    ${symbol_model_card["Account balance after trades ($)"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Number of trades taken:
                </Col>
                <Col>
                    {symbol_model_card["Number of trades taken"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Trades won:
                </Col>
                <Col>
                    {symbol_model_card["Trades won"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Trades lost:
                </Col>
                <Col>
                    {symbol_model_card["Trades lost"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Overall Win Rate:
                </Col>
                <Col>
                    {symbol_model_card["Overall Win Rate %"]} %
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Risk:Reward:
                </Col>
                <Col>
                    {symbol_model_card["Risk:Reward"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Stoploss Hits:
                </Col>
                <Col>
                    {symbol_model_card["Stoploss Hits"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Stoploss Misses:
                </Col>
                <Col>
                    {symbol_model_card["Stoploss Misses"]} <span style={{fontSize: '13px'}}>(closed in red but didn't hit the stoploss)</span>
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Takeprofit Misses:
                </Col>
                <Col>
                    {symbol_model_card["Takeprofit Misses"]} <span style={{fontSize: '13px'}}>(closed in blue but didn't hit the takeprofit)</span>
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Average number of consecutive wins:
                </Col>
                <Col>
                    {symbol_model_card["Average number of consecutive wins"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Average number of consecutive losses:
                </Col>
                <Col>
                    {symbol_model_card["Average number of consecutive losses"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Maximum number of consecutive wins:
                </Col>
                <Col>
                    {symbol_model_card["Maximum number of consecutive wins"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Maximum number of consecutive losses:
                </Col>
                <Col>
                    {symbol_model_card["Maximum number of consecutive losses"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Number of features:
                </Col>
                <Col>
                    {symbol_model_card["Number of features"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Training data start date:
                </Col>
                <Col>
                    {symbol_model_card["Training data start date"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Training data end date:
                </Col>
                <Col>
                    {symbol_model_card["Training data end date"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Training data number of trading days:
                </Col>
                <Col>
                    {symbol_model_card["Training data number of trading days"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Test data start date:
                </Col>
                <Col>
                    {symbol_model_card["Test data start date"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Test data end date:
                </Col>
                <Col>
                    {symbol_model_card["Test data end date"]}
                </Col>
            </Row>
            <br/>
            <Row style={{margin: '0px', textAlign: 'left'}}>
                <Col style={{fontWeight: 'bold'}}>
                    Test data number of trading days:
                </Col>
                <Col>
                    {symbol_model_card["Test data number of trading days"]}
                </Col>
            </Row>
            <br/>
        </div>
    );
};

export default ModelCardRender;
