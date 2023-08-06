from typing import List
from math import sin,cos

from scipy.stats import gmean, hmean
from scipy.fft import fftn
from numpy.linalg import norm
from numpy import (
    ndarray, concatenate, argmax, array,
    zeros, mean, sum, pad
)
import numpy

from ffast.poincare.token import Token
from ffast.poincare.utils import Poincare, METAPHONES, SIZE_METAPHONES
from ffast.wordnet.utils import STOPWORDS

class Tokens:
    def __init__(self, tokens:List[Token], pad_token_id:int) -> None:
        self.pad_token_id = pad_token_id
        self.tokens = tokens
        self.__pointer = -1
        self.ids = list(map(lambda token:token.id,self))
        self.vector = self.__sentence_embedding() if any(tokens) else None

    def __repr__(self) -> str:
        return '\n'.join(map(repr,self.tokens))
    
    def __str__(self) -> str:
        return ' '.join(map(str,self.tokens))

    def __len__(self) -> int:
        return len(self.tokens)

    def __iter__(self) -> "Tokens":
        return self
    
    def __next__(self) -> Token: 
        self.__pointer += 1
        if self.__pointer < len(self):
            return self.tokens[self.__pointer]
        raise StopIteration
    
    def __getitem__(self,index:int) -> Token:
        return self.tokens[index]

    def __round__(self, n:int) -> ndarray:
        return pad(self.ids, pad_width=(0,n), constant_values=self.pad_token_id)[:n]

    def semantics(self) -> List[ndarray]:
        return list(map(lambda token:token.semantics, self.tokens))
    
    def weights(self) -> List[float]:
        return list(map(self.__weight,self.tokens))

    def skip_common_words(self) -> "Tokens":
        return Tokens(list(filter(lambda token:self.__weight(token)>0.,self.tokens)),pad_token_id=self.pad_token_id)

    def skip_unknowns(self) -> "Tokens":
        return Tokens(list(filter(lambda token:token.morphology != Poincare.UNKNOWN.value,self.tokens)),pad_token_id=self.pad_token_id)

    def most_similar(self, others:List["Tokens"]) -> "Tokens":
        others_vectors = array(list(map(lambda other:other.vector, others)))
        index_best = argmax(others_vectors@self.vector)
        return others[index_best]

    def __sentence_embedding(self) -> ndarray:
        sparse_token_vectors = list(map(self.__embed_token,self.tokens))
        position_vectors = list(map(self.__embed_position,range(len(self.tokens))))
        contextual_token_vectors = sum([sparse_token_vectors,position_vectors],axis=0)
        dynamics_of_token_vectors = self.__fourier_transformation(sparse_token_vectors)
        return concatenate([
            self.__power_means(contextual_token_vectors),
            self.__power_means(dynamics_of_token_vectors)
        ])
        
    @staticmethod
    def __power_means(vectors:List[ndarray]) -> ndarray:
        positive_vectors = list(map(abs,vectors))
        return concatenate([
            numpy.max(vectors,axis=0),
            numpy.min(vectors,axis=0),
            mean(vectors,axis=0),
            gmean(positive_vectors),
            hmean(positive_vectors),
        ])
    
    @staticmethod
    def __fourier_transformation(vectors:List[ndarray]) -> ndarray:
        return abs(fftn(vectors))

    @staticmethod 
    def __embed_position(position:int) -> ndarray:
        SIZE_VECTOR = SIZE_METAPHONES + Poincare.SIZE_VECTOR.value
        position_vector = zeros(SIZE_VECTOR)
        for index in range(0,SIZE_VECTOR-1,2):
            angle = position/(1e5 ** ((2*index)/SIZE_VECTOR))
            position_vector[index]=sin(angle)
            position_vector[index+1]=cos(angle)
        return position_vector

    @staticmethod
    def __embed_token_phonetics(token:Token) -> ndarray:
        embedding = zeros(SIZE_METAPHONES)
        for character in token.phonology:
            metaphone_index = METAPHONES.index(character)
            embedding[metaphone_index] = 1
        return embedding

    @staticmethod
    def __embed_token_semantics(token:Token) -> ndarray:
        return token.semantics

    @staticmethod
    def __embed_token(token:Token) -> ndarray:
        return concatenate([
            Tokens.__embed_token_phonetics(token),
            Tokens.__embed_token_semantics(token),
        ])    
    
    @staticmethod
    def __weight(token:Token,minimum_weight:float = 0.,maximum_weight:float = 1.,scaling_factor:float = 10.) -> float:
        if token.text in STOPWORDS:
            return 0.
        approximation_of_token_frequency = .5 - norm(token.semantics)
        approximation_of_token_frequency *= scaling_factor
        return min(maximum_weight,max(minimum_weight,approximation_of_token_frequency))