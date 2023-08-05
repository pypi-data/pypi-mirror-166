__all__ = ('LocationEntityMetadata', 'ScheduledEventEntityMetadata', 'StageEntityMetadata')

from scarletio import RichAttributeErrorBaseType, copy_docs

from ..user import ClientUserBase, create_partial_user_from_id


def try_get_scheduled_event_metadata_type_from_data(data):
    """
    Tries to detect what type of scheduled metadata the given data is.
    
    Parameters
    ----------
    data : `dict` of (`str`, `str`) items
        Scheduled event metadata data.
    
    Returns
    -------
    metadata_type : `None`, `type`
    """
    if 'location' in data:
        metadata_type = LocationEntityMetadata
    elif 'speaker_ids' in data:
        metadata_type = StageEntityMetadata
    else:
        metadata_type = None
    
    return metadata_type


class ScheduledEventEntityMetadata(RichAttributeErrorBaseType):
    """
    Base class for ``ScheduledEvent``'s entity metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new entity metadata instance.
        """
        raise NotImplemented
        
    def __repr__(self):
        """Returns the entity metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event entity metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Entity metadata structure.
        
        Returns
        -------
        self : ``ScheduledEventEntityMetadata``
        """
        raise NotImplemented
    
    
    def to_data(self):
        """
        Converts the entity metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two entity metadatas equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the entity metadata's hash value."""
        return 0


class StageEntityMetadata(ScheduledEventEntityMetadata):
    """
    Stage entity metadata of ``ScheduledEvent``-s.
    
    Attributes
    ----------
    speaker_ids : `None`, `tuple` of `int`
        The speakers' identifier of the stage channel.
    """
    __slots__ = ('speaker_ids', )
    
    def __new__(cls, speakers):
        """
        Creates a new stage entity metadata for ``ScheduledEvent``-s.
        
        Parameters
        ----------
        speakers : `None`, `int`, ``ClientUserBase``, `iterable` of (`int`, `ClientUserBase``)
            Speakers of the stage channel.
        
        Raises
        ------
        TypeError
            - If `speakers` type is incorrect.
            - If a speaker's type is incorrect.
        """
        if speakers is None:
            speaker_ids = None
        
        elif isinstance(speakers, ClientUserBase):
            speaker_ids = (ClientUserBase.id, )
        
        elif isinstance(speakers, int):
            speaker_ids = (speakers, )
        
        else:
            iterator = getattr(type(speakers), '__iter__', None)
            if iterator is None:
                raise TypeError(
                    f'`speakers` can be `None`, `int`, `{ClientUserBase.__name__}`, `iterable` of (`int`, '
                    f'`{ClientUserBase.__name__}`), got {speakers.__class__.__name__}; {speakers!r}.'
                )
            
            speaker_ids = None
            
            for speaker in iterator(speakers):
                if isinstance(speaker, ClientUserBase):
                    speaker_id = speaker.id
                
                elif isinstance(speaker, int):
                    speaker_id = speaker
                
                else:
                    raise TypeError(
                        f'`speakers` can contain `int`, `{ClientUserBase.__name__}` elements, got '
                        f'{speaker.__class__.__name__}; {speaker!r}.'
                    )
                
                if speaker_ids is None:
                    speaker_ids = set()
                
                speaker_ids.add(speaker_id)
            
            if (speaker_ids is not None):
                speaker_ids = tuple(sorted(speaker_ids))
            
            else:
                speaker_ids = None
        
        self = object.__new__(cls)
        self.speaker_ids = speaker_ids
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadata.from_data)
    def from_data(cls, data):
        speaker_ids = data.get('speaker_ids', None)
        if (speaker_ids is None) or (not speaker_ids):
            speaker_ids = None
        else:
            speaker_ids = tuple(sorted(int(speaker_id) for speaker_id in speaker_ids))
        
        self = object.__new__(cls)
        self.speaker_ids = speaker_ids
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadata.to_data)
    def to_data(self):
        data = {}
        
        speaker_ids = self.speaker_ids
        if (speaker_ids is None):
            speaker_ids = ()
        data['speaker_ids'] = speaker_ids
        
        return data
    
    
    @copy_docs(ScheduledEventEntityMetadata.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.speaker_ids != other.speaker_ids:
            return False
        
        return True
    
    
    @copy_docs(ScheduledEventEntityMetadata.__hash__)
    def __hash__(self):
        hash_value = 0
        
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            hash_value ^= len(speaker_ids)
            
            for speaker_id in speaker_ids:
                hash_value ^= speaker_id
        
        return hash_value
    
    
    @property
    def iter_speaker_ids(self):
        """
        Iterates over the speakers' identifiers of the stage channel.
        
        This method is an iterable generator.
        
        Yields
        ------
        speaker_id : `int`
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            yield from speaker_ids
    
    @property
    def speakers(self):
        """
        Returns the speakers of the stage channel.
        
        Returns
        -------
        speakers : `None`, `tuple` of ``ClientUserBase``
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            return tuple(create_partial_user_from_id(speaker_id) for speaker_id in speaker_ids)
    
    
    def iter_speakers(self):
        """
        Iterates over the speakers of the stage channel.
        
        This method is an iterable generator.
        
        Yields
        ------
        speakers : ``ClientUserBase``
        """
        speaker_ids = self.speaker_ids
        if (speaker_ids is not None):
            
            for speaker_id in speaker_ids:
                yield create_partial_user_from_id(speaker_id)


class LocationEntityMetadata(ScheduledEventEntityMetadata):
    """
    Location entity metadata of ``ScheduledEvent``-s.
    
    Attributes
    ----------
    location : `None`, `str`
        The place where the event will take place.
    """
    __slots__ = ('location', )
    
    def __new__(cls, location):
        """
        Creates a new location entity metadata for ``ScheduledEvent``-s.
        
        Parameters
        ----------
        location : `str`
            The location.
        
        Raises
        ------
        TypeError
            If `location`'s type is incorrect.
        ValueError
            If `location` is an empty string.
        """
        if not isinstance(location, str):
            raise TypeError(
                f'`location` can be `str`, got {location.__class__.__name__}; {location!r}.'
            )
        
        if not location:
            raise ValueError(
                f'`location` cannot be empty string.'
            )
        
        self = object.__new__(cls)
        self.location = location
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadata.from_data)
    def from_data(cls, data):
        location = data.get('location', None)
        
        self = object.__new__(cls)
        self.location = location
        return self
    
    
    @classmethod
    @copy_docs(ScheduledEventEntityMetadata.to_data)
    def to_data(self):
        return {
            'location': self.location,
        }
    
    
    @copy_docs(ScheduledEventEntityMetadata.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.location != other.location:
            return False
        
        return True
    
    @copy_docs(ScheduledEventEntityMetadata.__hash__)
    def __hash__(self):
        hash_value = 0
        
        location = self.location
        if (location is not None):
            hash_value ^= hash(location)
        
        return hash_value
