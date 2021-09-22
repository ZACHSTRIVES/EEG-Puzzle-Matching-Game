import { render } from "@testing-library/react";
import React from "react";
import './lobby.css'
import logo from '../../static/logo.png'
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';


const Lobby = () => {
    const url = "http://demo.aucss.co.nz"

    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <div className="lobby">
            <img src={logo}></img>
            <div className="lobby-startButton" onClick={() => {
                window.location.href = url;
                return null;
            }}>
                START GAME
            </div>

            <div className="lobby-rules" onClick={handleClickOpen}>Rules of the game</div>

            <div className="lobby-notice">
                <Alert severity="error">
                    <AlertTitle>EEG device is not connected</AlertTitle>
                    The game will be played in beta mode — <strong>check it out!</strong>
                </Alert>


            </div>



            <Dialog
                open={open}
                onClose={handleClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    Matching Game Instructions

                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        This is the famous Memory game, known as Concentration card game or Matching Game. You should concentrate on completing the game to win high scores. You can play quietly, at your own pace, until you have found all the pairs. The object of the game is to find all the pairs with the fewest number of moves and in the shortest possible time.

                    </DialogContentText>
                    <p>
                        1. There are ten unique pairs of cards, making 20 cards total.
                    </p>
                    <p>
                        2. Cards are laid out in a 4×5 grid face down, all the cards are mixed up and laid in rows, face down on the table. You can flip any pair of cards on each turn.
                    </p>
                    <p>
                        3. If the two cards match, you score, the two cards are turned over and fixed, you can get to the next turn. If they do not match, the cards are turned back.
                    </p>
                    <p>
                        4. When cards are turned over, it is important to remember where they are for when the matching card is turned up later in the game.
                    </p>

                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Close</Button>

                </DialogActions>
            </Dialog>






        </div>
    )




}


export default Lobby;