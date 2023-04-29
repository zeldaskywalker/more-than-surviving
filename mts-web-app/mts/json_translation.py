from . import models
import json

def events_to_timeline_json(events, images):
    final_images_dict = {}
    for image in images:
        final_images_dict[image.image_id] = {
            'url': image.header_url,
            'caption': image.caption,
            'credit': image.credit,
            'alt': image.alt_text
        }


    final_timeline_dict = {}
    final_events_list = []
    for event in events:
        event_dict = {}

        first_image_id = event.image_ids[0]

        media_dict = final_images_dict[first_image_id]

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

        text_dict = {
            "headline": event.title,
            "text": event.short_description,
        }

        event_dict["text"] = text_dict
        final_events_list.append(event_dict)

    final_timeline_dict["events"] = final_events_list
    final_timeline_json_string = json.dumps(final_timeline_dict)
    final_timeline_json = json.loads(final_timeline_json_string)
    return final_timeline_json
