import { Request, Response } from 'express';
import { injectable } from 'tsyringe';
import { UserService } from '../services/UserService';

interface UserParams {
  id: string;
}

@injectable()
export class UserController {
  constructor(private userService: UserService) {}

  getUser = async (req: Request<UserParams>, res: Response) => {
    const user = await this.userService.getUser(req.params.id);

    res.json(user);
  };
}
