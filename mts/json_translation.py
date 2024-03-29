from . import models
from django.urls import path
import json

def event_date_string(start_date, end_date):
    if start_date == end_date:
        return f"{start_date}"
    else:
        return f"{start_date} - {end_date}"

def date_parser(date, date_accuracy):
    # Determine correct start date format for JSON based on accuracy
    if date_accuracy == 'DAY':
        return date.strftime("%B %-d, %Y")
    elif date_accuracy == 'MONTH':
        return date.strftime("%B, %Y")
    else:
        return date.strftime("%Y")

def create_images_dict(images):
    final_images_dict = {}
    for image in images:
        final_images_dict[image.image_id] = {
            'url': image.url,
            'gallery_url': image.gallery_url,
            'caption': image.caption,
            'credit': image.credit,
            'alt': image.alt_text,
        }
    return final_images_dict

def related_events_dict(events, images_dict):
    event_cards = []
    for event in events:
        event_card_info = {}
        start_date = event.start_date.strftime("%Y")
        end_date = event.end_date.strftime("%Y")
        date_string = event_date_string(start_date, end_date)
        location_string = ' + '.join(event.location_names)
        if event.image_ids:

            first_image_id = event.image_ids[0]
        else:
            first_image_id = 'MTSPlaceholder_image_1.jpg'
        html_issue_tags = ""
        for issue in event.issue_types:
            if issue == "Indigenous Rights":
                html_issue_tags += "<button id='indigenous-rights-button' disabled>INDIGENOUS RIGHTS</button> "
            elif issue == "Anti-Slavery":
                html_issue_tags += "<button id='anti-slavery-button' disabled>ANTI-SLAVERY</button> "
            elif issue == "Women's Rights":
                html_issue_tags += "<button id='womens-rights-button' disabled>WOMEN'S RIGHTS</button> "
            elif issue == "Temperance":
                html_issue_tags += "<button id='temperance-button' disabled>TEMPERANCE</button> "
            elif issue == "Racial Equality":
                html_issue_tags += "<button id='racial-equality-button' disabled>RACIAL EQUALITY</button> "

        event_card_info = {
            'title': event.title,
            'image_url': images_dict[first_image_id]['gallery_url'],
            'alt_text': images_dict[first_image_id]['alt'],
            'dates': date_string,
            'location': location_string,
            'button_path': f'/event/{event.event_id}',
            'issue_types': html_issue_tags,
        }
        event_cards.append(event_card_info)
    return event_cards

def related_activists_dict(activists, images_dict):
    activist_cards = []
    for activist in activists:
        activist_card_info = {}
        dob = activist.date_of_birth.strftime("%Y")
        dod = activist.date_of_death.strftime("%Y")
        date_string = event_date_string(dob, dod)
        location_string = ' + '.join(activist.tribal_affiliations)
        if activist.image_ids:
            first_image_id = activist.image_ids[0]
        else:
            first_image_id = 'MTSPlaceholder_image_1.jpg'

        html_issue_tags = ""
        for issue in activist.issue_types:
            if issue == "Indigenous Rights":
                html_issue_tags += "<button id='indigenous-rights-button' disabled>INDIGENOUS RIGHTS</button> "
            elif issue == "Anti-Slavery":
                html_issue_tags += "<button id='anti-slavery-button' disabled>ANTI-SLAVERY</button> "
            elif issue == "Women's Rights":
                html_issue_tags += "<button id='womens-rights-button' disabled>WOMEN'S RIGHTS</button> "
            elif issue == "Temperance":
                html_issue_tags += "<button id='temperance-button' disabled>TEMPERANCE</button> "
            elif issue == "Racial Equality":
                html_issue_tags += "<button id='racial-equality-button' disabled>RACIAL EQUALITY</button> "

        activist_card_info = {
            'title': activist.name,
            'image_url': images_dict[first_image_id]['gallery_url'],
            'alt_text': images_dict[first_image_id]['alt'],
            'dates': date_string,
            'location': location_string,
            'button_path': f'/activist/{activist.activist_id}',
            'issue_types': html_issue_tags
        }
        activist_cards.append(activist_card_info)
    return activist_cards

def gallery_view_dict(events, activists, images_dict):
    return related_events_dict(events, images_dict) + related_activists_dict(activists, images_dict)


def events_to_timeline_json(events, final_images_dict):

    final_timeline_dict = {}
    final_events_list = []
    for event in events:
        event_dict = {}

        if event.image_ids:
            first_image_id = event.image_ids[0]
            media_dict = final_images_dict[first_image_id]
            del media_dict['caption']
            if event.thumbnail:
                media_dict['thumbnail'] = final_images_dict[event.thumbnail]['url']

            event_dict["media"] = media_dict

        start_date_accuracy = event.start_date_accuracy
        end_date_accuracy = event.end_date_accuracy

        start_date_year = event.start_date.strftime("%Y")
        end_date_year = event.end_date.strftime("%Y")

        # Determine correct start date format for JSON based on accuracy
        if start_date_accuracy == 'DAY':
            start_date_month = event.start_date.strftime("%m")
            start_date_day = event.start_date.strftime("%d")
            start_date_dict = {
                "year": start_date_year,
                "month": start_date_month,
                "day": start_date_day,
            }
        elif start_date_accuracy == 'MONTH':
            start_date_month = event.start_date.strftime("%m")
            start_date_dict = {
                "year": start_date_year,
                "month": start_date_month,
            }
        else:
            start_date_dict = {
                "year": start_date_year,
            }

        event_dict["start_date"] = start_date_dict

        # Determine correct end date format for JSON based on accuracy
        if end_date_accuracy == 'DAY':
            end_date_month = event.end_date.strftime("%m")
            end_date_day = event.end_date.strftime("%d")
            end_date_dict = {
                "year": end_date_year,
                "month": end_date_month,
                "day": end_date_day,
            }
        elif end_date_accuracy == 'MONTH':
            end_date_month = event.end_date.strftime("%m")
            end_date_dict = {
                "year": end_date_year,
                "month": end_date_month,
            }
        else:
            end_date_dict = {
                "year": end_date_year,
            }

        event_dict["end_date"] = end_date_dict

        if event.event_id.startswith('CON'):
            final_description = event.short_description
        else:
            final_description = event.short_description + '<br>' + '<a class="caption" style="font-weight: 500; font-style: italic; font-size: 11px" href="/event/' + event.event_id+ '"><i><b>Continue reading</b></i></a>',

        text_dict = {
            "headline": event.title,
            "text": final_description
        }

        event_dict["text"] = text_dict
        if event.map == True:
            event_dict["group"] = "Wampanoag Activism"
        else:
            event_dict["group"] = "State and National Events"
        final_events_list.append(event_dict)

    final_timeline_dict["events"] = final_events_list
    final_timeline_json_string = json.dumps(final_timeline_dict)
    final_timeline_json = json.loads(final_timeline_json_string)
    return final_timeline_json

def events_to_map_geojson(events, images_dict):
    final_mapbox_dict = {"type": "FeatureCollection"}
    final_features_list = []
    for event in events:
        for location in event.location_names:
            feature_dict = {"type": "Feature"}

            first_image_id = event.image_ids[0]

            start_date = event.start_date.strftime("%Y")
            end_date = event.end_date.strftime("%Y")
            date_string = event_date_string(start_date, end_date)
            location_string = ' + '.join(event.location_names)
            
            html_issue_tags = ""
            for issue in event.issue_types:
                if issue == "Indigenous Rights":
                    html_issue_tags += "<button id='indigenous-rights-button' disabled>INDIGENOUS RIGHTS</button> "
                elif issue == "Anti-Slavery":
                    html_issue_tags += "<button id='anti-slavery-button' disabled>ANTI-SLAVERY</button> "
                elif issue == "Women's Rights":
                    html_issue_tags += "<button id='womens-rights-button' disabled>WOMEN'S RIGHTS</button> "
                elif issue == "Temperance":
                    html_issue_tags += "<button id='temperance-button' disabled>TEMPERANCE</button> "
                elif issue == "Racial Equality":
                    html_issue_tags += "<button id='racial-equality-button' disabled>RACIAL EQUALITY</button> "

            properties_dict = {
                "link_path": f'/event/{event.event_id}',
                "title": event.title,
                "description": event.short_description,
                "issue_type": event.issue_types[0],
                "issue_types": html_issue_tags,
                "image_url": images_dict[first_image_id]['url'],
                "image_alt_text": images_dict[first_image_id]['alt'],
                "date_string": date_string,
                "location": location_string
            }

            feature_dict["properties"] = properties_dict

            longitude = event.location_data[location]["longitude"]
            latitude = event.location_data[location]["latitude"]

            geometry_dict = {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }

            feature_dict["geometry"] = geometry_dict

            final_features_list.append(feature_dict)

    final_mapbox_dict["features"] = final_features_list
    final_mapbox_geojson_string = json.dumps(final_mapbox_dict)
    final_mapbox_geojson = json.loads(final_mapbox_geojson_string)
    return final_mapbox_geojson