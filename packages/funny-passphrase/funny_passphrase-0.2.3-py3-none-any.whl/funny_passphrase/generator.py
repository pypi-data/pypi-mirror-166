#!/usr/bin/env python
# -*- coding: utf-8 -*-

# funny_passphrase, a library to index text files, and generate
# passphrases from them.
# Copyright (C) 2022 Barcelona Supercomputing Center, José M. Fernández
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from typing import (
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Union,
)

from .indexer import CompressedIndexedText


class FunnyPassphraseGenerator(object):
    """
    This class takes as input a sequence of CompressedIndexedText
    instances, which can be considered groups of words.
    It generates a passphrase in the form of a random word from each
    group of words. If the number of words is larger than the number of
    groups, the generator loops over the groups of words.
    """

    def __init__(self, *args: CompressedIndexedText, **kwargs: CompressedIndexedText):
        cit: MutableSequence[CompressedIndexedText]
        cit_dict: MutableMapping[str, CompressedIndexedText]
        if args:
            cit = list(arg for arg in args)
            cit_dict = dict((str(i_arg), arg) for i_arg, arg in enumerate(args))
        else:
            cit = list()
            cit_dict = dict()

        if kwargs:
            cit_dict.update(kwargs)
            cit.extend(kwargs.values())

        self.cit = cit
        self.cit_dict: MutableMapping[str, CompressedIndexedText] = cit_dict

    def __len__(self) -> int:
        """
        It returns the number of different word sets
        """
        return len(self.cit)

    def word_set_tags(self) -> Sequence[Union[str, int]]:
        """
        It returns the symbolic names of the word sets
        """
        return list(self.cit_dict.keys())

    def generate(
        self, num: int = 5, subset: Optional[Sequence[Union[str, int]]] = None
    ) -> Iterator[str]:
        """
        This method allows generating a passphrase, based either in all
        the word sets received on instantiation, or using an ordered subset
        """
        cit_dict: Union[
            Sequence[CompressedIndexedText],
            Mapping[str, CompressedIndexedText],
        ]
        subset_l: Union[Sequence[int], Sequence[str]]
        if subset:
            subset_l = list(str(s) for s in subset)
            cit_dict = self.cit_dict
            for s_name in subset_l:
                if s_name not in cit_dict:
                    raise KeyError(
                        f"Word set {s_name} is not among the available ones ({cit_dict.keys()})"
                    )

            # Duplicated block to avoid mypy complains
            for cit_idx in range(num):
                real_cit_idx = cit_idx % len(subset_l)
                cI = cit_dict[subset_l[real_cit_idx]]
                yield cI.get_random_line()
        else:
            # Suboptimal but effective
            subset_l = list(range(len(self)))
            cit = self.cit

            # Duplicated block to avoid mypy complains
            for cit_idx in range(num):
                real_cit_idx = cit_idx % len(subset_l)
                cI = cit[subset_l[real_cit_idx]]
                yield cI.get_random_line()

    def generate_passphrase(
        self,
        sep: str = " ",
        num: int = 5,
        subset: Optional[Sequence[Union[str, int]]] = None,
    ) -> str:
        """
        This method allows generating a passphrase,
        using the given separator
        """
        return sep.join(self.generate(num=num, subset=subset))
