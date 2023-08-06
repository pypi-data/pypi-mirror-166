# hpc-sdk
sdk for hpc app of EU Materials-MarketPlace

## Interacte with HPC through MarketPlace proxy

### Use/integrate HPC Gateway app by SDK

This repository provide SDK for using or integrating the HPC gateway app into other MarketPlace app.

First, create a `hpc` instance with:

python
```
from marketplace_hpc import HpcGatewayApp

hpc = HpcGatewayApp(
    client_id=<app_id>, # This is the HPC gateway app.
    access_token=<your_access_token>,
)
```

The following capabilities are supported and can be called by using the SDK.

- Check the availability of system: `hpc.heartbeat()`
- Create a new calculation: `hpc.new_job()`, the resourceid will returned to list files on remote workdir, upload/downlead/delete files and the launch/delete job.
- Upload file: `hpc.upload_file(resourceid=<resourceid>, source_path=<file_local_path>`.
- Download file: `hpc.download_file(resourceid=<resourceid>, filename=<filename>`.
- Delete file: `hpc.delete_file(resourceid=resourceid, filename=<filename>)`
- List jobs (only CSCS deployment): `hpc.list_jobs()`.
- Launch job: `hpc.run_job(resourceid=<resourceid>)`
- Delete job: `hpc.delete_job(resourceid=resourceid)`

You can find example at https://github.com/materials-marketplace/hpc-sdk/blob/main/hpc_api.ipynb

### Materials Cloud (CSCS) deployment

The correspond HPC-Gateway app is https://www.materials-marketplace.eu/app/hpc-app (ID: `5fd66c68-50e9-474a-b55d-148777ae3efd`) deployed on production server.

Since it deployed using Materials Cloud CSCS resources provided by EPFL, it is only for test purpose and MarketPlace users who what to use it need to contact Jusong Yu @unkpcz (jusong.yu@epfl.ch) to add your MarketPlace account to the whitelist and then register your account by:

```
curl -X POST \
   -H "Authorization:Bearer <put_your_token_here>" \
   'https://mp-hpc.herokuapp.com/user'
```

### IWM deployment

The correspond HPC-Gateway app is [HPC gateway (broker)](https://staging.materials-marketplace.eu/app/hpc-gateway-broker) (ID: `dc67d85e-7945-49fa-bf85-3159a8358f85`) deployed on staging server since RPC broker server needed.

## For maintainers

To create a new release, clone the repository, install development dependencies with `pip install '.[dev]'`, and then execute `bumpver update`.
This will:

  1. Create a tagged release with bumped version and push it to the repository.
  2. Trigger a GitHub actions workflow that creates a GitHub release.

Additional notes:

  - Use the `--dry` option to preview the release change.
  - The release tag (e.g. a/b/rc) is determined from the last release.
    Use the `--tag` option to switch the release tag.

## Acknowledgements

This work is supported by the
the MARKETPLACE project funded by [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) under the H2020-NMBP-25-2017 call (Grant No. 760173),

<div style="text-align:center">
 <img src="miscellaneous/logos/MarketPlace.png" alt="MarketPlace" height="75px">
</div>
