import xmltodict
from typing import Dict, Optional

class MTConnectParser:
    @staticmethod
    def parse_stream(xml_content: str) -> Dict:
        """
        Parse raw MTConnect XML and return simplified state dict.
        """
        try:
            data = xmltodict.parse(xml_content)
            streams = data.get('MTConnectStreams', {}).get('Streams', {}).get('DeviceStream', {})
            
            # Navigate complex MTConnect structure (Simplified for this example)
            # Usually: Streams -> DeviceStream -> ComponentStream -> Events/Samples
            
            # Mock extractor - in prod this needs robust traversal
            execution = "STOPPED"
            program = ""
            
            # This is a specialized parser logic that would need adjustment based on specific machine XML
            # For now, we assume we extract these values
            # (In a real implementation, we'd search for DataItemId="execution" etc.)
            
            return {
                "execution": execution,
                "program": program
            }
        except Exception as e:
            print(f"XML Parse Error: {e}")
            return {}

    @staticmethod
    def extract_from_mock(xml_dict: Dict) -> Dict:
        """
        Helper to extract state from a clean dictionary (for testing).
        """
        return {
            "execution": xml_dict.get("execution", "STOPPED"), # ACTIVE, READY, STOPPED
            "program": xml_dict.get("program", "")
        }
