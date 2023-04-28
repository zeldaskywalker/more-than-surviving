import json

def translate_sql_data_to_timeline_json(query_result_list):
    final_timeline_dict = {}
    final_events_list = []
    for row in query_result_list:
        event_dict = {}

        media_dict = {
            "url": row[9],
            "caption": row[10],
            "credit": row[11],
            "alt": row[12]
        }

        event_dict["media"] = media_dict

        start_date_accuracy = row[3]
        end_date_accuracy = row[5]

        start_date_year = row[2].strftime("%Y")
        end_date_year = row[4].strftime("%Y")

        # Determine correct start date format for JSON based on accuracy
        if start_date_accuracy == 'day':
            start_date_month = row[2].strftime("%m")
            start_date_day = row[2].strftime("%d")
            start_date_dict = {
                "year": start_date_year,
                "month": start_date_month,
                "day": start_date_day,
                }
        elif start_date_accuracy == 'month':
            start_date_month = row[2].strftime("%m")
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
        if end_date_accuracy == 'day':
            end_date_month = row[4].strftime("%m")
            end_date_day = row[4].strftime("%d")
            end_date_dict = {
                "year": end_date_year,
                "month": end_date_month,
                "day": end_date_day,
                }
        elif end_date_accuracy == 'month':
            end_date_month = row[4].strftime("%m")
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
            "headline": row[1],
            "text": row[7],
        }

        event_dict["group"] = 1

        final_events_list.append(event_dict)

    final_timeline_dict["events"] = final_events_list
    final_timeline_json_string = json.dumps(final_timeline_dict)
    final_timeline_json = json.loads(final_timeline_json_string)
    return final_timeline_json

import json

def translate_sql_data_to_geo_json(query_result_list):
  final_mapbox_dict = {"type": "FeatureCollection"}
  final_features_list = []
  for row in query_result_list:
    feature_dict = {"type": "Feature"}

    properties_dict = {
        "id": row[0],
        "title": row[1],
        "description": row[5],
        "issue_types": row[6],
        "thumbnail": row[7],
        "activists": row[8],
        "location": row[4]
    }

    feature_dict["properties"] = properties_dict

    geometry_dict = {
        "type": "Point",
        "coordinates": [row[3], row[2]]
    }

    feature_dict["geometry"] = geometry_dict

    final_features_list.append(feature_dict)

  final_mapbox_dict["features"] = final_features_list
  final_mapbox_geojson_string = json.dumps(final_mapbox_dict)
  final_mapbox_geojson = json.loads(final_mapbox_geojson_string)
  return final_mapbox_geojson