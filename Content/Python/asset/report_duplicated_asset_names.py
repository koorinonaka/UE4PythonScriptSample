import unreal
import sys

from utilities.asset_library import ProcessSlotTask

unreal.log(sys.argv)


class ReportDuplicatedAssetNames(object):

    dict_key_check = {}
    dict_duplicates = {}

    def check_duplicate(self, asset_data):
        asset_name = asset_data.asset_name
        package_name = asset_data.package_name

        if asset_name in self.dict_key_check:
            if asset_name not in self.dict_duplicates:
                self.dict_duplicates[asset_name] = {}

            first = self.dict_key_check[asset_name].package_name
            self.dict_duplicates[asset_name][first] = True

            self.dict_duplicates[asset_name][package_name] = True

        else:
            self.dict_key_check[asset_name] = asset_data

    def report(self, asset_name, package_names):
        unreal.log('===== duplicated: {}'.format(asset_name))
        for package_name in package_names:
            unreal.log(unreal.StringLibrary.conv_name_to_string(
                package_name).encode('utf-8'))

    def execute(self):
        search_path = "/Game/"
        try:
            search_path += sys.argv[1]
        except IndexError:
            pass

        if unreal.EditorAssetLibrary.does_directory_exist(search_path) != True:
            unreal.log_warning(
                'search directory is not found: {}'.format(search_path))
            return

        all_assets = filter(
            lambda x: x.is_redirector != True,
            unreal.AssetRegistryHelpers
            .get_asset_registry()
            .get_assets_by_path(unreal.Paths.normalize_directory_name(search_path), True)
        )

        ProcessSlotTask.execute(
            'checking all assets',
            lambda x: self.check_duplicate(x),
            all_assets
        )

        for asset_name in self.dict_duplicates:
            paths = list(self.dict_duplicates[asset_name].keys())
            paths.sort()
            self.report(asset_name, paths)


ReportDuplicatedAssetNames().execute()
