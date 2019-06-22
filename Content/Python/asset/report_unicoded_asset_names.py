import unreal
import sys

from utilities.asset_library import ProcessSlotTask

unreal.log(sys.argv)


class ReportUnicodedAssetNames(object):

    def check_asset_name(self, asset_data):
        package_name = unreal.StringLibrary.conv_name_to_string(
            asset_data.package_name)

        if isinstance(package_name, unicode):
            unreal.log('package name has unicode: {}'.format(
                package_name.encode('utf-8')))

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

        ProcessSlotTask.execute(
            'checking name of asset',
            lambda x: self.check_asset_name(x),
            unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(
                unreal.Paths.normalize_directory_name(search_path), True)
        )


ReportUnicodedAssetNames().execute()
