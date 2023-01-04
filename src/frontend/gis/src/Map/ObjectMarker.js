import { Avatar, List, ListItem, ListItemIcon, ListItemText } from "@mui/material";
import FlagIcon from '@mui/icons-material/Flag';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import ContactsIcon from '@mui/icons-material/Contacts';
import React from "react";
import { Marker, Popup } from 'react-leaflet';
import { icon as leafletIcon, point } from "leaflet";

const defaultUrl = "https://cdn-icons-png.flaticon.com/512/447/447031.png"

const LIST_PROPERTIES = [
    { "key": "class", label: "Class", Icon: FlagIcon },
    { "key": "country_id", label: "Country ID", Icon: ContactsIcon },
    { "key": "horario_id", label: "Horario ID", Icon: PictureInPictureAltIcon },
    { "key": "iata", label: "IATA", Icon: FlagIcon },
    { "key": "icao", label: "ICAO", Icon: ContactsIcon },
    { "key": "pes", label: "PES", Icon: ContactsIcon },
    { "key": "fonte", label: "FONTE", Icon: ContactsIcon },


];

export function ObjectMarker({ geoJSON }) {
    const properties = geoJSON?.properties
    const { id, imgUrl, name } = properties;
    const coordinates = geoJSON?.geometry?.coordinates;

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: imgUrl || defaultUrl,
                iconRetinaUrl: imgUrl || defaultUrl,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgUrl || defaultUrl} />
                        </ListItemIcon>
                        <ListItemText primary={name} />
                    </ListItem>
                    {
                        LIST_PROPERTIES
                            .map(({ key, label, Icon }) =>
                                <ListItem key={key}>
                                    <ListItemIcon>
                                        <Icon style={{ color: "black" }} />
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={<span>
                                            {properties[key]}<br />
                                            <label style={{ fontSize: "xx-small" }}>({label})</label>
                                        </span>}
                                    />
                                </ListItem>
                            )
                    }

                </List>

            </Popup>
        </Marker>
    )
}