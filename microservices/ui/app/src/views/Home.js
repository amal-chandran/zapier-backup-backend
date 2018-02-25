import React, { Component } from "react";
import {
    Icon, AppBar, Typography, Toolbar,
    Grid, Paper, withStyles, IconButton, Menu, MenuItem
} from "material-ui";
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import arrow from "./../assets/arrow.svg";
import { Wrapper, Uploader } from "./../components";
import config from "./../config/config.json";
import { authHelper } from "./../helper";
import { authActions, notifiActions } from "./../actions";
import { push } from 'react-router-redux'


class Home extends Component {
    state = {
        anchorEl: null,
    };

    handleMenu = event => {
        this.setState({ anchorEl: event.currentTarget });
    };

    handleClose = () => {
        this.setState({ anchorEl: null });
    };

    render() {
        const { classes } = this.props;
        const { anchorEl } = this.state;
        const open = Boolean(anchorEl);
        const headers = authHelper.getHeader(false);

        return (
            <div>
                <AppBar classes={{ root: classes.AppBar_root }} position="static" color="primary">
                    <Wrapper>
                        <Toolbar classes={{ root: classes.Toolbar_root }}>
                            <Typography className={classes.flex} variant="title" color="inherit">Zapper</Typography>

                            <div>
                                {/* <IconButton>
                                    <Icon>cloud_upload</Icon>
                                </IconButton> */}
                                <IconButton
                                    aria-owns={open ? 'menu-appbar' : null}
                                    aria-haspopup="true"
                                    onClick={this.handleMenu}
                                    color="inherit"
                                >
                                    <Icon>account_circle</Icon>
                                </IconButton>
                                <Menu
                                    id="menu-appbar"
                                    anchorEl={anchorEl}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={open}
                                    onClose={this.handleClose}
                                >
                                    <MenuItem onClick={this.handleClose}>Profile</MenuItem>
                                    <MenuItem onClick={(e) => {
                                        this.props.actions.push("/");
                                        this.handleClose(e);
                                    }}>Logout</MenuItem>
                                </Menu>
                            </div>
                        </Toolbar>
                    </Wrapper>
                </AppBar>

                <Wrapper>

                    <div className="filesArea">
                        <Uploader
                            url={config.url.upload}
                            // auto
                            xhrOptions={
                                {
                                    headers
                                }
                            }
                            onResponce={(err, res, body) => {
                                const { actions } = this.props;
                                body = JSON.parse(body);

                                if (res.statusCode === 200 && "message" in body) {
                                    actions.addNotifi(body.message, "success");
                                } else if (res.statusCode === 400 && "message" in body) {
                                    actions.addNotifi(body.message, "error");
                                } else if ("message" in body) {
                                    actions.addNotifi(body.message, "info");
                                }
                            }}
                        />

                    </div>
                </Wrapper>
            </div>
        );
    }
};

const style = {
    AppBar_root: {
        boxShadow: "none",
        background: "#68c368",
        boxShadow: "0 0 6px #68c368",
        borderBottom: "1px solid #3eb13e"
    },
    Toolbar_root: {
        padding: "0px"
    },
    flex: {
        flex: 1,
    },
    Icon_root: {
        fontSize: "100px",
        color: "gray"
    }
};

const mapDispatchToProps = (dispatch) => {
    const addNotifi = notifiActions.addNotifi;
    return {
        actions: bindActionCreators({
            addNotifi, push
        }, dispatch)
    }
};

export default withStyles(style)(connect(() => { return {}; }, mapDispatchToProps)(Home));