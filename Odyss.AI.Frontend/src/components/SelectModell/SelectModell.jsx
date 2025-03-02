import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import styles from './SelectModell.module.css';

export default function SelectModell({setSelectedModel}) {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = (model) => {
        setAnchorEl(null);
        setSelectedModel(model);
    };

    return (
        <div className={styles.selectModell}>
            <Button
                id="basic-button"
                aria-controls={open ? 'basic-menu' : undefined}
                aria-haspopup="true"
                aria-expanded={open ? 'true' : undefined}
                onClick={handleClick}
            >
                Wähle Modell
            </Button>
            <Menu
                id="basic-menu"
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                MenuListProps={{
                    'aria-labelledby': 'basic-button',
                }}
            >
                <MenuItem onClick={() => handleClose("mistral")}>Mistral</MenuItem>
                <MenuItem onClick={() => handleClose("chatgpt")}>ChatGPT</MenuItem>
            </Menu>
        </div>
    );
}
