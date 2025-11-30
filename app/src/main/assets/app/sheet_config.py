"""
Configuration for Game Sheet Layout and Styling.
"""

SHEET_CONFIG = {
    "game_title": {
        "textFormat": {
            "fontSize": 14,
            "bold": True
        },
        "horizontalAlignment": "LEFT",
        "verticalAlignment": "MIDDLE"
    },
    "tournament_name": {
        "textFormat": {
            "fontSize": 12,
            "italic": True
        },
        "horizontalAlignment": "LEFT",
        "verticalAlignment": "MIDDLE"
    },
    "player_names": {
        "textFormat": {
            "fontSize": 12,
            "bold": True
        },
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    },
    "total_scores": {
        "textFormat": {
            "fontSize": 12,
            "bold": True
        },
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    },
    "headers": {
        "textFormat": {
            "fontSize": 9,
            "bold": True
        },
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE"
    },
    "columns": {
        "cards_dealt": {
            "pixelSize": 40
        },
        "bid": {
            "pixelSize": 40
        },
        "won": {
            "pixelSize": 40
        },
        "score": {
            "pixelSize": 40
        }
    }
}
