"""

    """

import json
import shutil
from pathlib import Path

import pandas as pd
from dulwich import index
from dulwich import porcelain
from dulwich.client import HTTPUnauthorized

from src.githubdata.consts import data_file_suffixes
from src.githubdata.consts import github_base_url
from src.githubdata.funcs import clean_github_url
from src.githubdata.funcs import get_github_token_pathes
from src.githubdata.funcs import get_usr_tok_from_jsp
from src.githubdata.funcs import github_url_wt_credentials


class GithubData :
    def __init__(self , source_url , user_token_json_path = None) :
        self.source_url = source_url
        self._usr_tok_jsp = user_token_json_path

        self.cln_src_url = clean_github_url(source_url)
        self.user_repo = self.cln_src_url.split(github_base_url)[1]
        self.user_name = self.user_repo.split('/')[0]
        self.repo_name = self.user_repo.split('/')[1]

        self._local_path = None

        self._clone_url = None

        self._cred_usr = None
        self._cred_tok = None

        self._commit_url = None

        self._repo = None
        self._data_suf = None
        self.data_fp = None
        self.meta = None
        self.meta_fp = None

        self._init_local_path()
        self.set_data_fps()
        self.read_metadata()

    @property
    def local_path(self) :
        return self._local_path

    @local_path.setter
    def local_path(self , local_dir) :
        if local_dir is None :
            self._local_path = Path(self.repo_name)
        else :
            self._local_path = Path(local_dir) / self.repo_name

        if self._local_path.exists() :
            print('Warning: local_path already exists')

    def _init_local_path(self) :
        self.local_path = None

    def _stage_all_changes(self) :
        idx = self._repo.open_index()

        lp = self.local_path
        fu = porcelain.get_untracked_paths
        untracked = fu(lp , lp , idx , exclude_ignored = True)

        unstaged = index.get_unstaged_changes(idx , self.local_path)

        all_changes = list(unstaged) + list(untracked)

        self._repo.stage(all_changes)

    def _set_defualt_data_suffix(self) :
        for ky in data_file_suffixes.keys() :
            fps = self.ret_sorted_fpns_by_suf(ky)
            if len(fps) >= 1 :
                self._data_suf = ky
                break

    def set_data_fps(self) :
        self._set_defualt_data_suffix()

        if self._data_suf is None :
            return None

        fpns = self.ret_sorted_fpns_by_suf(self._data_suf)

        if len(fpns) == 1 :
            self.data_fp = fpns[0]
        else :
            self.data_fp = fpns

    def ret_sorted_fpns_by_suf(self , suffix) :
        suffix = '.' + suffix if suffix[0] != '.' else suffix
        the_list = list(self._local_path.glob(f'*{suffix}'))
        return sorted(the_list)

    def read_metadata(self) :
        fps = self.ret_sorted_fpns_by_suf('.json')
        if len(fps) == 0 :
            return None
        fp = fps[0]
        self.meta_fp = fp
        with open(fp , 'r') as fi :
            js = json.load(fi)
        self.meta = js
        return js

    def _input_cred_usr_tok(self) :
        usr = input('(enter nothing for same as repo source) github username: ')
        if usr.strip() == '' :
            self._cred_usr = self.user_name
        tok = input('token: ')
        self._cred_tok = tok

    def _set_cred_usr_tok(self) :
        if self._usr_tok_jsp is not None :
            fp = self._usr_tok_jsp
            self._cred_usr , self._cred_tok = get_usr_tok_from_jsp(fp)
            return None

        fp = Path('user_token.json')
        if fp.exists() :
            self._cred_usr , self._cred_tok = get_usr_tok_from_jsp(fp)
            return None

        fp = get_github_token_pathes()
        if fp :
            self._cred_usr , self._cred_tok = get_usr_tok_from_jsp(fp)
            return None

        self._input_cred_usr_tok()

    def _set_clone_url(self) :
        self._set_cred_usr_tok()
        usr = self._cred_usr
        tok = self._cred_tok
        tr = self.user_repo
        self._clone_url = github_url_wt_credentials(usr , tok , tr)

    def overwriting_clone(self , depth = 1) :
        """ Every time excecuted, it re-downloads last version of the reposiroty to local_path.

        param depth: None for full depth, default = 1 (last version)
        return: None
        """
        trgdir = self.local_path
        if trgdir.exists() :
            self.rmdir()

        try :
            self._clone_url = self.cln_src_url
            url = self._clone_url
            self._repo = porcelain.clone(url , trgdir , depth = depth)
        except HTTPUnauthorized :
            self._set_clone_url()
            url = self._clone_url
            self._repo = porcelain.clone(url , trgdir , depth = depth)

        self.set_data_fps()
        self.read_metadata()

    def _set_commit_url(self) :
        if self._clone_url != self.cln_src_url :
            self._commit_url = self._clone_url
        else :
            self._set_cred_usr_tok()
            usr = self._cred_usr
            tok = self._cred_tok
            tr = self.user_repo
            self._commit_url = github_url_wt_credentials(usr , tok , tr)

    def commit_and_push(self , message , branch = 'main') :
        self._set_commit_url()
        self._stage_all_changes()
        self._repo.do_commit(message.encode())
        porcelain.push(str(self._local_path) , self._commit_url , branch)

    def read_data(self) :
        if not self._local_path.exists() :
            self.overwriting_clone()
        else :
            self.set_data_fps()
        if not isinstance(self.data_fp , list) :
            if self._data_suf == '.xlsx' :
                # noinspection PyArgumentList
                return pd.read_excel(self.data_fp)
            else :
                return pd.read_parquet(self.data_fp)

    def rmdir(self) :
        shutil.rmtree(self._local_path)
