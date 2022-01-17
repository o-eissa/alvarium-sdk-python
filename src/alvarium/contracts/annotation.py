import ulid
import json

from typing import List
from dataclasses import dataclass, field
from enum import Enum
from alvarium.hash.contracts import HashType
from datetime import datetime, timezone

class AnnotationType(Enum):
    TPM = "tpm"
    PKI = "pki"
    TLS = "tls"
    SOURCE = "src"
    MOCK = "mock"

    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class Annotation:
    """A data class that encapsulates all of the data related to a specific annotation.
    this will be generated by the annotators."""

    key: str
    hash: HashType
    host: str
    kind: AnnotationType 
    timestamp: str = field(default_factory=lambda : datetime.now(timezone.utc).astimezone().isoformat(), init=True) 
    id: ulid.ULID = field(default_factory=ulid.new, init=True)
    is_satisfied: bool = None
    signature: str = None

    def to_json(self) -> str:
        annotation_json = {"id": str(self.id), "key": str(self.key), "hash": str(self.hash),
                           "host": str(self.host), "kind": str(self.kind),
                           "timestamp": str(self.timestamp)}
        
        if self.signature != None:
            annotation_json["signature"] = str(self.signature)
        
        if self.is_satisfied != None:
            annotation_json["isSatisfied"] = self.is_satisfied

        return json.dumps(annotation_json)

    @staticmethod
    def from_json(data: str):
        annotation_json = json.loads(data)
        return Annotation(id=ulid.from_str(annotation_json["id"]), key=annotation_json["key"],
                          hash=HashType(annotation_json["hash"]), host=annotation_json["host"],
                          kind=AnnotationType(annotation_json["kind"]), signature=annotation_json["signature"],
                          is_satisfied=bool(annotation_json["isSatisfied"]), timestamp=annotation_json["timestamp"])

    def __str__(self) -> str:
        return self.to_json() 


@dataclass
class AnnotationList:
    items: List[Annotation]

    def to_json(self) -> str:
        annotation_list_json = {"items": [json.loads(str(item)) for item in self.items]}
        return json.dumps(annotation_list_json)
    
    @staticmethod
    def from_json(data: str):
        annotation_list_json = json.loads(data)
        return AnnotationList(items=[Annotation.from_json(json.dumps(item)) for item in annotation_list_json["items"]])

    def __str__(self) -> str:
        return self.to_json() 
    